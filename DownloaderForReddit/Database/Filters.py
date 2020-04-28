import traceback
from abc import ABC
from sqlalchemy.sql import func
from sqlalchemy import and_, or_
from sqlalchemy import desc as descending

from .Models import RedditObjectList, RedditObject, DownloadSession, Post, Content, Comment, ListAssociation


class Filter(ABC):

    """
    An abstract class that filters database model queries based on a list of supplied tuples that correspond to model
    attributes.
    """

    op_map = {
        'eq': lambda attr, value: attr == value,
        'lt': lambda attr, value: or_(attr == None, attr < value),
        'lte': lambda attr, value: or_(attr == None, attr <= value),
        'gt': lambda attr, value: attr > value,
        'gte': lambda attr, value: attr >= value,
        'in': lambda attr, value: attr.in_(value),
        'like': lambda attr, value: attr.like(value),
        'wild_like': lambda attr, value: attr.like(f'%{value}%'),
        'contains': lambda attr, value: attr.contains(value)
    }

    model = None
    default_order = 'id'

    session = None

    def __init__(self):
        self.custom_filter_map = {}
        self.order_map = {}

    def filter(self, session, *filters, query=None, order_by=None, desc=False):
        self.session = session
        if query is None:
            query = session.query(self.model)
        for tup in filters:
            key, operator, value = tup
            attr = getattr(self.model, key, None)
            if not attr:
                query = self.custom_filter(query, key, operator, value)
                continue
            if operator == 'in':
                if not isinstance(value, list):
                    value = value.split(',')
            try:
                f = self.op_map[operator](attr, value)
                query = query.filter(f)
            except Exception as e:
                print(e)
        if order_by is None:
            order_by = self.default_order
        if desc:
            order_by = descending(order_by)
        return query.order_by(order_by)

    def custom_filter(self, query, attr, operator, value):
        try:
            return self.custom_filter_map[attr](query, operator, value)
        except KeyError:
            return query


class RedditObjectListFilter(Filter):

    model = RedditObjectList
    default_order = 'name'

    def __init__(self):
        super().__init__()
        self.custom_filter_dict = {
            'reddit_object_count': self.reddit_object_count_filter,
        }

    def reddit_object_count_filter(self, query, operator, value):
        ros = self.session.query(ListAssociation.reddit_object_list_id,
                                 func.count(ListAssociation.reddit_object_id).label('ro_count'))\
            .group_by(ListAssociation.reddit_object_list_id).subquery()
        f = self.op_map[operator](ros.c.ro_count, value)
        query = query.outerjoin(ros, RedditObjectList.id == ros.c.reddit_object_list_id).filter(f)
        return query


class RedditObjectFilter(Filter):

    model = RedditObject
    default_order = 'name'

    def __init__(self):
        super().__init__()
        self.custom_filter_dict = {
            'post_score': self.post_score_filter,
            'post_count': self.post_count_filter,
            'comment_score': self.comment_score_filter,
            'comment_count': self.comment_count_filter,
            'content_count': self.content_count_filter,
            'download_count': self.download_count_filter,
        }

    def post_score_filter(self, query, operator, value):
        posts = self.session.query(Post.significant_reddit_object_id, func.sum(Post.score).label('total_score'))\
            .group_by(Post.significant_reddit_object_id).subquery()
        f = self.op_map[operator](posts.c.total_score, value)

        query = query.outerjoin(posts, RedditObject.id == posts.c.significant_reddit_object_id).filter(f)
        return query

    def post_count_filter(self, query, operator, value):
        posts = self.session.query(Post.significant_reddit_object_id, func.count(Post.id).label('post_count'))\
            .group_by(Post.significant_reddit_object_id).subquery()
        f = self.op_map[operator](posts.c.post_count, value)
        query = query.outerjoin(posts, RedditObject.id == posts.c.significant_reddit_object_id).filter(f)
        return query

    def comment_score_filter(self, query, operator, value):
        comments = self.session.query(Post.significant_reddit_object_id, func.sum(Comment.score).label('total_score'))\
            .join(Post).group_by(Post.significant_reddit_object_id).subquery()
        f = self.op_map[operator](comments.c.total_score, value)
        query = query.outerjoin(comments, RedditObject.id == comments.c.significant_reddit_object_id).filter(f)
        return query

    def comment_count_filter(self, query, operator, value):
        comments = self.session.query(Post.significant_reddit_object_id, func.count(Comment.id).label('comment_count'))\
            .join(Post).group_by(Post.significant_reddit_object_id).subquery()
        f = self.op_map[operator](comments.c.comment_count, value)
        query = query.outerjoin(comments, RedditObject.id == comments.c.significant_reddit_object_id).filter(f)
        return query

    def content_count_filter(self, query, operator, value):
        content = self.session.query(Post.significant_reddit_object_id, func.count(Content.id).label('content_count'))\
            .join(Post).group_by(Post.significant_reddit_object_id).subquery()
        f = self.op_map[operator](content.c.content_count, value)
        query = query.outerjoin(content, RedditObject.id == content.c.significant_reddit_object_id).filter(f)
        return query

    def download_count_filter(self, query, operator, value):
        s = self.session.query(Post.significant_reddit_object_id,
                               func.count(Post.download_session_id.distinct()).label('dl_count'))\
            .group_by(Post.significant_reddit_object_id).subquery()
        f = self.op_map[operator](s.c.dl_count, value)
        query = query.outerjoin(s, RedditObject.id == s.c.significant_reddit_object_id).filter(f)
        return query


class DownloadSessionFilter(Filter):

    model = DownloadSession
    default_order = 'id'

    def __init__(self):
        super().__init__()
        self.custom_filter_dict = {
            'reddit_object_count': self.reddit_object_count_filter,
            'post_count': self.post_count_filter,
            'comment_count': self.comment_count_filter,
            'content_count': self.content_count_filter,
        }

    def reddit_object_count_filter(self, query, operator, value):
        ros = self.session.query(Post.download_session_id,
                                 func.count(Post.significant_reddit_object_id.distinct()).label('ro_count'))\
            .group_by(Post.download_session_id).subquery()
        f = self.op_map[operator](ros.c.ro_count, value)
        query = query.outerjoin(ros, DownloadSession.id == ros.c.download_session_id).filter(f)
        return query

    def post_count_filter(self, query, operator, value):
        posts = self.session.query(Post.download_session_id, func.count(Post.id).label('post_count')) \
            .group_by(Post.download_session_id).subquery()
        f = self.op_map[operator](posts.c.post_count, value)
        query = query.outerjoin(posts, DownloadSession.id == posts.c.download_session_id).filter(f)
        return query

    def comment_count_filter(self, query, operator, value):
        comments = self.session.query(Post.download_session_id, func.count(Comment.id).label('comment_count')) \
            .join(Post).group_by(Post.download_session_id).subquery()
        f = self.op_map[operator](comments.c.comment_count, value)
        query = query.outerjoin(comments, DownloadSession.id == comments.c.download_session_id).filter(f)
        return query

    def content_count_filter(self, query, operator, value):
        content = self.session.query(Post.download_session_id, func.count(Content.id).label('content_count')) \
            .join(Post).group_by(Post.download_session_id).subquery()
        f = self.op_map[operator](content.c.content_count, value)
        query = query.outerjoin(content, DownloadSession.id == content.c.download_session_id).filter(f)
        return query


class PostFilter(Filter):

    model = Post
    default_order = 'title'

    def __init__(self):
        super().__init__()
        self.custom_filter_dict = {
            'comment_count': self.comment_count_filter,
            'content_count': self.content_count_filter,
        }

    def comment_count_filter(self, query, operator, value):
        comments = self.session.query(Comment.post_id, func.count(Comment.id).label('comment_count'))\
            .group_by(Comment.post_id).subquery()
        f = self.op_map[operator](comments.c.comment_count, value)
        query = query.outerjoin(comments, Post.id == comments.c.post_id).filter(f)
        return query

    def content_count_filter(self, query, operator, value):
        content = self.session.query(Content.post_id, func.count(Content.id).label('content_count'))\
            .group_by(Content.post_id).subquery()
        f = self.op_map[operator](content.c.content_count, value)
        query = query.outerjoin(content, Post.id == content.c.post_id).filter(f)
        return query


class ContentFilter(Filter):

    model = Content
    default_order = 'title'

    def __init__(self):
        super().__init__()
        self.custom_filter_dict = {
            'post_score': self.post_score_filter,
            'post_date': self.post_date_filter,
            'nsfw': self.nsfw_filter,
            'domain': self.domain_filter,
        }

    def post_score_filter(self, query, operator, value):
        f = self.op_map[operator](Post.score, value)
        query = query.join(Post).filter(f)
        return query

    def post_date_filter(self, query, operator, value):
        f = self.op_map[operator](Post.date_posted, value)
        query = query.join(Post).filter(f)
        return query

    def nsfw_filter(self, query, operator, value):
        f = self.op_map[operator](Post.nsfw, value)
        query = query.join(Post).filter(f)
        return query

    def domain_filter(self, query, operator, value):
        f = self.op_map[operator](Post.domain, value)
        query = query.join(Post).filter(f)
        return query


class CommentFilter(Filter):

    model = Comment
    default_order = 'id'

    def __init__(self):
        super().__init__()
        self.custom_filter_map = {
            'post_score': self.post_score_filter,
            'post_date': self.post_date_filter,
            'nsfw': self.nsfw_filter,
        }

    def post_score_filter(self, query, operator, value):
        f = self.op_map[operator](Post.score, value)
        query = query.join(Post).filter(f)
        return query

    def post_date_filter(self, query, operator, value):
        f = self.op_map[operator](Post.date_posted, value)
        query = query.join(Post).filter(f)
        return query

    def nsfw_filter(self, query, operator, value):
        f = self.op_map[operator](Post.nsfw, value)
        query = query.join(Post).filter(f)
        return query
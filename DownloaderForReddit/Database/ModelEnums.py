from enum import Enum


class DisplayableEnum(Enum):

    @property
    def display_name(self):
        return self.name.replace('_', ' ')


class DownloadNameMethod(DisplayableEnum):

    ID = 1
    TITLE = 2
    AUTHOR_NAME = 3


class SubredditSaveStructure(DisplayableEnum):

    SUB_NAME = 1
    AUTHOR_NAME = 2
    SUB_NAME_AUTHOR_NAME = 3
    AUTHOR_NAME_SUB_NAME = 4


class CommentDownload(DisplayableEnum):

    DOWNLOAD = 1
    DO_NOT_DOWNLOAD = 2
    DOWNLOAD_ONLY_AUTHOR = 3


class NsfwFilter(DisplayableEnum):

    EXCLUDE = -1
    INCLUDE = 0
    ONLY = 1


class LimitOperator(DisplayableEnum):

    LESS_THAN = -1
    NO_LIMIT = 0
    GREATER_THAN = 1


class RedditObjectSortMethod(DisplayableEnum):

    ID = 1
    NAME = 2
    SCORE = 3
    POST_COUNT = 4
    CONTENT_COUNT = 5
    DATE_ADDED = 6
    DATE_CREATED = 7
    LAST_DOWNLOAD = 8
    LAST_POST_DATE = 9


class PostSortMethod(DisplayableEnum):

    NEW = 1
    HOT = 2
    RISING = 3
    CONTROVERSIAL = 4
    TOP_HOUR = 5
    TOP_DAY = 6
    TOP_WEEK = 7
    TOP_MONTH = 8
    TOP_YEAR = 9
    TOP_ALL = 10


class CommentSortMethod(DisplayableEnum):

    NEW = 1
    TOP = 2
    BEST = 3
    CONTROVERSIAL = 4
    OLD = 5

import os
import requests
import logging
from concurrent.futures import ThreadPoolExecutor

from ..Utils import Injector, SystemUtil, VideoMerger
from ..Database.Models import Content


class Downloader:

    """
    Class that is responsible for the actual downloading of content.
    """

    def __init__(self, download_queue, download_session_id):
        """
        Initializes the Downloader class.
        :param download_queue: A queue of Content items that are to be downloaded.
        :type download_queue: Queue
        """
        self.logger = logging.getLogger(f'DownloaderForReddit.{__name__}')
        self.download_queue = download_queue
        self.download_session_id = download_session_id
        self.output_queue = Injector.get_output_queue()
        self.db = Injector.get_database_handler()
        self.settings_manager = Injector.get_settings_manager()

        self.thread_count = self.settings_manager.download_thread_count
        self.executor = ThreadPoolExecutor(self.thread_count)
        self.continue_run = True
        self.download_count = 0

    def run(self):
        """
        Removes content from the queue and sends it to the thread pool executor for download until it is told to stop.
        """
        while self.continue_run:
            content = self.download_queue.get()
            if content is not None:
                self.executor.submit(self.download, content=content)
            else:
                self.continue_run = False
        self.executor.shutdown(wait=True)

    def download(self, content: Content):
        """
        Connects to the content url and downloads the content item to the file path specified by the content item.
        :param content: The content item which is to be downloaded.
        """
        try:
            response = requests.get(content.url, stream=True)
            if response.status_code == 200:
                content.make_download_title()
                file_path = content.full_file_path
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(1024 * 1024):
                        file.write(chunk)
                self.finish_download(content)
            else:
                self.handle_unsuccessful_response(content, response.status_code)
        except ConnectionError:
            self.handle_connection_error(content)
        except:
            self.handle_unknown_error(content)

    def check_file_path(self, content: Content):
        """
        Checks the content's full file path to make sure there are no naming conflicts.  If there are, a number is
        incremented and appended to the contents title until a naming conflict no longer exists.
        :param content: The Content item who's path is to be checked.
        """
        unique_count = 1
        path = content.full_file_path
        while os.path.exists(path):
            content.title = f'{content.title}({unique_count})'
            path = content.full_file_path
            unique_count += 1

    def finish_download(self, content: Content):
        """
        Wraps up loose ends from the download process.  Takes care of updating the user about the download status,
        setting the date modified for the file, and saving the content changes to the database.
        :param content: The content item that has been downloaded and needs to be finished.
        """
        if self.settings_manager.set_file_modified_date:
            SystemUtil.set_file_modify_time(content.full_file_path, content.post.date_posted.timestamp())
        self.check_video_merger(content)
        content.set_downloaded(self.download_session_id)
        self.output_queue.put(f'Saved: {content.full_file_path}')

    def check_video_merger(self, content: Content):
        """
        If the content item has a video merge id, this method takes care of setting the correct settings in the
        VideoMerger so that the parts can be successfully merged later.
        :param content: The content item that may need to be merged.
        """
        if content.video_merge_id is not None:
            try:
                ms = VideoMerger.videos_to_merge[content.video_merge_id]
                if content.extension == 'mp4':
                    ms.video_path = content.full_file_path
                else:
                    ms.audio_path = content.full_file_path
            except KeyError:
                self.logger.error('Failed to add file to video merge list.  A merge set with this id does not exist.',
                                  extra={'merge_id': content.video_merge_id, 'filename': content.full_file_path})

    def handle_unsuccessful_response(self, content: Content, status_code):
        message = 'Failed Download: Unsuccessful response from server'
        self.log_errors(content, message, status_code=status_code)
        self.output_error(content, message)
        content.set_download_error(f'{message}: status_code: {status_code}')

    def handle_connection_error(self, content: Content):
        message = 'Failed Download: Failed to establish download connection'
        self.log_errors(content, message)
        self.output_error(content, message)
        content.set_download_error(message)

    def handle_unknown_error(self, content: Content):
        message = 'An unknown error occurred during download'
        self.log_errors(content, message)
        self.output_error(content, message)
        content.set_download_error(message)

    def log_errors(self, content: Content, message, **kwargs):
        extra = {'url': content.url, 'submission_id': content.post.reddit_id, 'user': content.user,
                 'subreddit': content.subreddit, 'save_path': content.full_file_path, **kwargs}
        self.logger.error(message, extra=extra, exc_info=True)

    def output_error(self, content, message):
        output_append = f'\nPost: {content.post.title}\nUrl: {content.url}\nUser: {content.user}\n' \
                        f'Subreddit: {content.subreddit}\n'
        self.output_queue.put(message + output_append)
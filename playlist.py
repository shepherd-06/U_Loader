import logging

from pytube import request

from single_file import Main

logger = logging.getLogger(__name__)

# -*- coding: utf-8 -*-
"""
Module to download a complete playlist from a youtube channel
"""


class Playlist(object):
    """Handles all the task of manipulating and downloading a whole YouTube
    playlist
    """

    def __init__(self, url):
        self.playlist_url = url
        self.video_urls = []

    def construct_playlist_url(self):
        """There are two kinds of playlist urls in YouTube. One that
        contains watch?v= in URL, another one contains the "playlist?list="
        portion. It is preferable to work with the later one.

        :return: playlist url -> string
        """

        if 'watch?v=' in self.playlist_url:
            base_url = 'https://www.youtube.com/playlist?list='
            playlist_code = self.playlist_url.split('&list=')[1]
            return base_url + playlist_code

        # url is already in the desired format, so just return it
        return self.playlist_url

    def parse_links(self):
        """Parse the video links from the page source, extracts and
        returns the /watch?v= part from video link href
        It's an alternative for BeautifulSoup

        :return: list
        """

        url = self.construct_playlist_url()
        req = request.get(url)

        # split the page source by line and process each line
        content = [x for x in req.split('\n') if 'pl-video-title-link' in x]
        link_list = [x.split('href="', 1)[1].split('&', 1)[0] for x in content]

        return link_list

    def populate_video_urls(self):
        """Construct complete links of all the videos in playlist and
        populate video_urls list

        :return: urls -> string
        """

        base_url = 'https://www.youtube.com'
        link_list = self.parse_links()

        for video_id in link_list:
            complete_url = base_url + video_id
            self.video_urls.append(complete_url)

    def get_all_url(self):
        """Download all the videos in the the playlist. Initially, download
        resolution is 720p (or highest available), later more option
        should be added to download resolution of choice
        """

        self.populate_video_urls()
        logger.debug('total videos found: ', len(self.video_urls))
        logger.debug('starting download')
        print(self.video_urls)
        return self.video_urls


if __name__ == '__main__':
    test_playlist = 'https://www.youtube.com/watch?v=76k991G0sJo&list=PLnd9zkUqwBehPFy-4seB_lWdqKhVa1EYT'
    url_list = Playlist(test_playlist).get_all_url()
    print(url_list)

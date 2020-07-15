from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

import styles.marine_dark as mk
import styles.green_light as gl
import sys
import os
import humanize
import re
import pafy

interface, _ = loadUiType('youtube.ui')


class Application(QMainWindow, interface):
    def __init__(self, parent = None):
        super(Application, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.ui_initial()
        self.ui_playlist()
        self.ui_single()
        self.ui_batch()
        self.ui_buttons()

    def ui_initial(self):
        # it contains all ui changes
        
        self.setWindowIcon(QIcon('icons\ysr.ico'))
        self.tabs.setCurrentIndex(0)
        self.logo.setText('')
        self.tabs.tabBar().setVisible(False)
        self.setFixedSize(1090, 650)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.status.setText('')

    def theme(self):
        current_theme = self.comboBox_theme.currentIndex()

        if current_theme == 0:
            self.setStyleSheet(gl.style_data)
        elif current_theme == 1:
            self.setStyleSheet(mk.style_data)

    def ui_buttons(self):
        # it contains all changes of buttons

        ########## THEME #############

        self.theme_button.clicked.connect(self.theme)
        self.quit.clicked.connect(QApplication.quit)
        self.minimize.clicked.connect(self.showMinimized)

        self.go_button.clicked.connect(self.go)
        self.single_tab.setVisible(False)
        self.batch_tab.setVisible(False)
        self.playlist_tab.setVisible(False)
        self.about_tab.setVisible(False)
        self.settings_tab.setVisible(False)

        ############ TABS ####################

        self.single_tab.clicked.connect(self.single)
        self.batch_tab.clicked.connect(self.batch)
        self.playlist_tab.clicked.connect(self.playlist)
        self.about_tab.clicked.connect(self.about)
        self.settings_tab.clicked.connect(self.settings)

    def go(self):
        self.single()
        self.batch_tab.setVisible(True)
        self.playlist_tab.setVisible(True)
        self.about_tab.setVisible(True)
        self.settings_tab.setVisible(True)

    def single(self):
        self.single_tab.setVisible(True)
        self.tabs.setCurrentIndex(1)
        self.logo.setText('Youtube Squeezer')

    def batch(self):
        self.batch_tab.setVisible(True)
        self.logo.setText('Youtube Squeezer')
        self.tabs.setCurrentIndex(2)

    def playlist(self):
        self.playlist_tab.setVisible(True)
        self.logo.setText('Youtube Squeezer')
        self.tabs.setCurrentIndex(3)

    def about(self):
        self.logo.setText('Youtube Squeezer')
        self.tabs.setCurrentIndex(5)
        self.status.setText('')

    def settings(self):
        self.tabs.setCurrentIndex(4)
        self.status.setText('')
        self.logo.setText('Youtube Squeezer')

    ##################### PLAYLIST ###############################

    def ui_playlist(self):
        self.urlText.setText('')
        self.browseText.setText('')
        self.error_url.setText('')
        self.error_browse.setText('')
        self.browseText.setEnabled(False)
        self.browseButton.setEnabled(False)
        self.type_combobox.setEnabled(False)

        self.downloadButton.clicked.connect(self.download_playlist)
        self.browseButton.clicked.connect(self.browse_directory_playlist)
        # self.resetButton.clicked.connect(self.reset)
        self.getButton.clicked.connect(self.get_play_list)
        self.select_all.clicked.connect(self.selecting_all_playlist)
        self.deselect_all.clicked.connect(self.deselecting_all_playlist)
        self.playlist_list.itemSelectionChanged.connect(
            self.select_me_playlist)

    original_playlist_links = []
    items_duplicates = []
    items_lists = []
    youtube_matching_links = {}

    def get_play_list(self):
        print('get_play function started')

        self.playlist_list.clear()
        playlist_url = self.urlText.text()

        print(f'playlist url = {playlist_url}')

        if playlist_url == '':
            self.error_url.setText('Please enter Valid Playlist Video URL')
        else:
            try:
                # DISABLING
                self.error_url.setText('')

                # ENABLING
                self.status.setText(
                    'Started Getting Playlist Details........Wait !!!!')

                self.browseText.setEnabled(True)
                self.browseButton.setEnabled(True)
                self.type_combobox.setEnabled(True)

                # PLAYLIST CREATION

                playlist_to_youtube_urls = []

                playlist = pafy.get_playlist(playlist_url)
                playlist_videos = playlist['items']
                playlist_title = playlist['title']

                lengths = len(playlist['items'])
                index = 0

                while index < lengths:
                    play_links = str(playlist['items'][index]['pafy'])
                    seps = play_links.split(' ')[2]
                    links = f'https://www.youtube.com/watch?v={seps}'
                    playlist_to_youtube_urls.append(links)
                    index += 1

                print(playlist_to_youtube_urls)
                print('playlist links created successfully')

                ############################ LOOPS INTEGRATION  ###################################

                # EMPTY LISTS

                titles_links = []

                # LIST TITLES ASSIGNING

                for title in playlist_videos:
                    name = title['playlist_meta']['title']
                    titles_links.append(name)
                    self.playlist_list.addItem(f'{name}')
                    QApplication.processEvents()

                print('playlist titles added to titles_links')

                # MATCHING LINKS THROUGH DICTIONARY

                youtube_dicts = dict(
                    zip(titles_links, playlist_to_youtube_urls))
                self.youtube_matching_links.update(youtube_dicts)
                print(
                    f'youtube_matching_links = {self.youtube_matching_links}')
                print(
                    f'Titles and urls merged to dictionary successfully to youtube_matching_links')

                ################################### ASSIGNING CODE TO GUI ################################

                self.playlist_title.setText(f'Title : {playlist_title}')
                self.playlist_number.setText(str(len(playlist_videos)))
                self.status.setText('Got Playlist Details')

            except Exception:
                print('exception error in get_play function')
                self.error_url.setText('Please enter Valid Url')
                return

        print('get_play function finished \n')

    def select_me_playlist(self):
        for item in self.playlist_list.selectedItems():
            self.items_duplicates.append(item.text())
        QApplication.processEvents()

        # DUPLICATES REMOVING

        print('duplicates_removing started')

        xyz = [self.items_lists.append(
            x) for x in self.items_duplicates if x not in self.items_lists]

        print('duplicates_removing finished \n')
        print(f'items_list = {xyz}')

    def browse_directory_playlist(self):

        print('browse directory function  started')

        url = self.urlText.text()

        if url == '':
            self.browseText.setEnabled(False)
            self.browseButton.setEnabled(False)
            print('browse directory not created')
        else:
            self.browseText.setEnabled(True)
            self.browseButton.setEnabled(True)

            browse_location = QFileDialog.getExistingDirectory(
                self, 'Select Destination Folder')
            self.browseText.setText(str(browse_location))
            print(
                f'browse directory created successfully =  {browse_location}')

        print('browse directory function  finished \n')

    def download_playlist(self):

        # ORIGINAL YOUTUBE LINKS

        if self.items_lists != '':
            for item in self.items_lists:
                for key, value in self.youtube_matching_links.items():
                    if item == key:
                        self.original_playlist_links.append(value)
                    QApplication.processEvents()
            print(f'original_playlist_links = {self.original_playlist_links}')
            print('original playlist links created successfully')

        elif self.items_lists == '':
            print('playlist list did not select any items')

        print('download_directory function started')

        save_location = self.browseText.text()

        if save_location == '':
            print('Please provide folder location')
        else:
            try:
                playlist_url = self.urlText.text()
                playlist = pafy.get_playlist(playlist_url)
                playlist_title = playlist['title']

                os.chdir(save_location)

                print(f'directory changed to save location : {save_location}')

                file_name = re.sub(r'[\\/*?:"<>|]', "", playlist_title)
                print(f'Playlist file_name = {file_name}')

                location = f'{save_location}/Youtube Squeezer/{file_name}'

                if os.path.exists(location):
                    os.chdir(location)
                    print('path already exists and changing to existing directory')
                else:
                    os.makedirs(location)
                    os.chdir(location)
                    print('directory created and moved to new directory')

            except Exception:
                print('Please Provide Valid folder location')
        print('download_directory function finished \n')

        type_selected = self.type_combobox.currentIndex()

        print('download_playlist function started')
        directory = str(os.getcwd())
        print(directory)

        print(f'directory changed to current directory : {directory} ')

        self.batch_tab.setEnabled(False)
        self.single_tab.setEnabled(False)

        if type_selected == 0:
            try:
                for link in self.original_playlist_links:
                    paf_youtube = pafy.new(link)
                    stream = paf_youtube.getbest(preftype = 'mp4')

                    title = paf_youtube.title
                    duration = paf_youtube.duration
                    size = humanize.naturalsize(stream.get_filesize())

                    print(f'{title} download started')
                    self.video_audio_title.setText(f'Video : {title}')
                    self.duration.setText(f'Duration : {duration}')
                    self.size_file.setText(f'Size : {size}')

                    stream.download(filepath = directory,
                                    callback = self.playlist_progress)
                    QApplication.processEvents()
                    print(f'{title}  download finished')

                    self.batch_tab.setEnabled(True)
                    self.single_tab.setEnabled(True)

            except Exception:
                print('Information provided is not sufficient')
        elif type_selected == 1:
            try:
                for link in self.original_playlist_links:
                    paf_youtube = pafy.new(link)
                    stream = paf_youtube.getbestaudio(preftype = 'm4a')

                    title = paf_youtube.title
                    duration = paf_youtube.duration
                    size = humanize.naturalsize(stream.get_filesize())

                    print(f'{title} download started')
                    self.video_audio_title.setText(f'Video : {title}')
                    self.duration.setText(f'Duration : {duration}')
                    self.size_file.setText(f'Size : {size}')

                    stream.download(filepath = directory,
                                    callback = self.playlist_progress)
                    QApplication.processEvents()

                    print(f'{title}  download finished')

                    self.batch_tab.setEnabled(True)
                    self.single_tab.setEnabled(True)

            except Exception:
                print('Information provided is not sufficient')

        print('download_playlist function finished')

    def playlist_progress(self, total, received, ratio, rate, time):
        if total > 0:
            download_percent = int(round(received * 100 / total))
            self.progressBar_playlist.setValue(download_percent)
            remaining_time = round(time / 60, 2)

            self.status.setText(
                str(f'Time Remaining : {remaining_time} mins and Downloaded - {download_percent}%'))
            QApplication.processEvents()

    def selecting_all_playlist(self):
        self.playlist_list.selectAll()

    def deselecting_all_playlist(self):
        self.playlist_list.clearSelection()

    ##################### SINGLE ###############################

    def ui_single(self):
        self.urlText_single.setText('')
        self.browseText_single.setText('')
        self.error_url_single.setText('')
        self.error_browse_single.setText('')
        self.video_radioButton.setChecked(True)
        self.status.setText('')

        self.getButton_single.clicked.connect(self.get_single)
        self.browseButton_single.clicked.connect(self.browse_directory_single)
        self.video_radioButton.toggled.connect(self.video_checked)
        self.audio_radioButton.toggled.connect(self.audio_checked)
        self.downloadButton_single.clicked.connect(self.download_single)
        self.resetButton_single.clicked.connect(self.reset_single)

    def get_single(self):
        single_url = self.urlText_single.text()

        try:
            if single_url == '':
                self.error_url_single.setText('Please Enter Youtube URL')
            else:
                single_video = pafy.new(single_url)
                streaming_video = single_video.videostreams
                streaming_audio = single_video.audiostreams

                for video in streaming_video:
                    video_size = humanize.naturalsize(video.get_filesize())
                    video_data = f'{video.extension} - {video.quality} - {video_size}'
                    self.video_combobox_single.addItem(video_data)

                for audio in streaming_audio:
                    audio_size = humanize.naturalsize(audio.get_filesize())
                    audio_data = f'{audio.extension} - {audio.quality} - {audio_size}'
                    self.audio_combobox_single.addItem(audio_data)

                title = single_video.title
                duration = single_video.duration

                self.video_audio_title_single.setText(f'Video/ Audio: {title}')
                self.duration_single.setText(f'Duration : {duration}')

                self.browseText_single.setEnabled(True)
                self.browseButton_single.setEnabled(True)
                self.video_combobox_single.setEnabled(True)

        except Exception:
            self.error_url_single.setText('Please Enter Valid Youtube URL')

    def browse_directory_single(self):
        print('browse directory function  started')

        url = self.urlText_single.text()

        if url == '':
            self.browseText_single.setEnabled(False)
            self.browseButton_single.setEnabled(False)
            print('browse directory not created')
        else:
            self.browseText_single.setEnabled(True)
            self.browseButton_single.setEnabled(True)

            browse_location = QFileDialog.getExistingDirectory(
                self, 'Select Destination Folder')
            self.browseText_single.setText(str(browse_location))
            print(
                f'browse directory created successfully =  {browse_location}')

            self.downloadButton_single.setEnabled(True)
            self.resetButton_single.setEnabled(True)

        print('browse directory function  finished \n')

    def download_single(self):
        url = self.urlText_single.text()
        location = self.browseText_single.text()

        try:
            if url == '' or location == '':
                self.status.setText(
                    'Please enter valid url or valid save location')
            else:

                self.batch_tab.setEnabled(False)
                self.playlist_tab.setEnabled(False)

                audio_radio = self.audio_radioButton.isChecked()

                os.chdir(location)

                if audio_radio:
                    audio_index = self.audio_combobox_single.currentIndex()

                    file_location = location + r'/Youtube Squeezer/SINGLE/Audio'

                    if os.path.exists(file_location):
                        os.chdir(file_location)
                    else:
                        os.makedirs(file_location)
                        os.chdir(file_location)

                    print('audio path created successfully')

                    audio = pafy.new(url)
                    streams = audio.audiostreams
                    download = streams[audio_index].download(
                        file_location, callback = self.single_progress)

                    self.batch_tab.setEnabled(True)
                    self.playlist_tab.setEnabled(True)

                else:
                    video_index = self.video_combobox_single.currentIndex()

                    file_location = location + r'/Youtube Squeezer/SINGLE/Video'
                    print(file_location)

                    if os.path.exists(file_location):
                        os.chdir(file_location)
                        print(os.getcwd())
                    else:
                        os.makedirs(file_location)
                        os.chdir(file_location)
                        print(os.getcwd())

                    print('video path created successfully')

                    video = pafy.new(url)
                    streams = video.videostreams
                    download = streams[video_index].download(
                        file_location, callback = self.single_progress)

                    self.batch_tab.setEnabled(True)
                    self.playlist_tab.setEnabled(True)

        except Exception:
            self.status.setText('Please enter Valid Details')

    def single_progress(self, total, received, ratio, rate, time):
        if total > 0:
            download_percent = int(round(received * 100 / total))
            self.progressBar_single.setValue(download_percent)
            remaining_time = round(time / 60, 2)

            self.status.setText(
                str(f'Time Remaining : {remaining_time} mins and Downloaded - {download_percent}%'))
            QApplication.processEvents()

    def video_checked(self):
        self.video_combobox_single.setEnabled(True)
        self.audio_combobox_single.setEnabled(False)

    def audio_checked(self):
        self.video_combobox_single.setEnabled(False)
        self.audio_combobox_single.setEnabled(True)

    def reset_single(self):
        self.urlText_single.setText('')
        self.browseText_single.setText('')
        self.video_audio_title_single.setText('')
        self.duration_single.setText('')
        self.error_url_single.setText('')
        self.error_browse_single.setText('')
        self.video_combobox_single.clear()
        self.audio_combobox_single.clear()
        self.progressBar_single.setValue(0)

        self.browseText_single.setEnabled(False)
        self.browseButton_single.setEnabled(False)
        self.video_combobox_single.setEnabled(False)
        self.audio_combobox_single.setEnabled(False)
        self.downloadButton_single.setEnabled(False)
        self.progressBar_single.setEnabled(False)

    ##################### BATCH ###############################

    def ui_batch(self):
        self.urlText_batch.setText('')
        self.browseText_batch.setText('')
        self.error_url_batch.setText('')
        self.error_browse_batch.setText('')

        self.batch_add_button.clicked.connect(self.batch_add)
        self.delete_batch.clicked.connect(self.batch_delete)
        self.browseButton_batch.clicked.connect(self.batch_browse)
        self.downloadButton__batch.clicked.connect(self.batch_download)
        self.resetButton_batch.clicked.connect(self.reset_batch)

    batch_dict = {}

    def batch_add(self):
        batch_url = self.urlText_batch.text()

        try:
            if batch_url == '':
                self.error_url_batch.setText('Enter Url')
            else:

                self.batch_list.setEnabled(True)
                self.delete_batch.setEnabled(True)
                self.browseText_batch.setEnabled(True)
                self.browseButton_batch.setEnabled(True)

                youtube_link = pafy.new(batch_url)
                video_title = youtube_link.title
                self.batch_dict.update({str(video_title):str(batch_url)})
                self.batch_list.addItem(video_title)

                self.urlText_batch.setText('')
        except Exception:
            self.error_url_batch.setText('Enter Valid Url')

    def batch_delete(self):
        for item in self.batch_list.selectedItems():
            self.batch_list.takeItem(self.batch_list.row(item))
        QApplication.processEvents()

    def batch_browse(self):
        batch_url = self.urlText_batch.text()
        items = [self.batch_list.item(i).text()
                 for i in range(self.batch_list.count())]

        try:
            if items == '':
                self.error_url_batch.setText('Enter Url')
            else:
                location = QFileDialog.getExistingDirectory(
                    self, 'Select Destination Folder')
                self.browseText_batch.setText(location)

                self.type_combobox_batch.setEnabled(True)
                self.resetButton_batch.setEnabled(True)
                self.downloadButton__batch.setEnabled(True)
                self.progressBar_batch.setEnabled(True)

        except Exception:
            self.error_browse_batch.setText(
                'Please provide Valid File Location')

    def batch_download(self):
        location = self.browseText_batch.text()
        index = self.type_combobox_batch.currentIndex()

        print(index)

        items = [self.batch_list.item(i).text()
                 for i in range(self.batch_list.count())]

        links = []

        for x in items:
            for y in self.batch_dict.keys():
                if x == y:
                    link = self.batch_dict[y]
                    links.append(link)

        os.chdir(location)

        self.single_tab.setEnabled(False)
        self.playlist_tab.setEnabled(False)

        if index == 1:
            file_location = location + r'/Youtube Squeezer/BATCH/Audios'

            if os.path.exists(file_location):
                os.chdir(file_location)
            else:
                os.makedirs(file_location)
                os.chdir(file_location)

            for link in links:
                paf_youtube = pafy.new(link)
                stream = paf_youtube.getbest(preftype = 'm4a')

                title = paf_youtube.title
                duration = paf_youtube.duration
                size = humanize.naturalsize(stream.get_filesize())

                print(f'{title} download started')
                self.video_audio_title_batch.setText(f'Video : {title}')
                self.duration_batch.setText(f'Duration : {duration}')
                self.size_file_batch.setText(f'Size : {size}')

                stream.download(filepath = file_location,
                                callback = self.batch_progress)
                QApplication.processEvents()
                print(f'{title}  download finished')
        else:
            file_location = location + r'/Youtube Squeezer/BATCH/Videos'

            if os.path.exists(file_location):
                os.chdir(file_location)
            else:
                os.makedirs(file_location)
                os.chdir(file_location)

            for link in links:
                paf_youtube = pafy.new(link)
                stream = paf_youtube.getbest(preftype = 'mp4')

                title = paf_youtube.title
                duration = paf_youtube.duration
                size = humanize.naturalsize(stream.get_filesize())

                print(f'{title} download started')
                self.video_audio_title_batch.setText(f'Video : {title}')
                self.duration_batch.setText(f'Duration : {duration}')
                self.size_file_batch.setText(f'Size : {size}')

                stream.download(filepath = file_location,
                                callback = self.batch_progress)
                QApplication.processEvents()
                print(f'{title}  download finished')

        self.single_tab.setEnabled(True)
        self.playlist_tab.setEnabled(True)

    def batch_progress(self, total, received, ratio, rate, time):
        if total > 0:
            download_percent = int(round(received * 100 / total))
            self.progressBar_batch.setValue(download_percent)
            remaining_time = round(time / 60, 2)

            self.status.setText(
                str(f'Time Remaining : {remaining_time} mins and Downloaded - {download_percent}%'))
            QApplication.processEvents()

    def reset_batch(self):
        self.urlText_single.setText('')
        self.browseText_single.setText('')
        self.video_audio_title_single.setText('')
        self.duration_single.setText('')
        self.size_file_single.setText('')
        self.error_url_single.setText('')
        self.error_browse_single.setText('')

        self.browseText_single.setEnabled(False)
        self.browseButton_single.setEnabled(False)
        self.video_combobox_single.setEnabled(False)
        self.audio_combobox_single.setEnabled(False)
        self.downloadButton_single.setEnabled(False)
        self.progressBar_single.setEnabled(False)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(gl.style_data)
    window = Application()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

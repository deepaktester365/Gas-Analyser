import urllib.request
import re
import os
import datetime
import pandas as pd

text_file_name = "Items.csv"

class Item(object):
    def __init__(self):
        name = None
        url = ""
        price = None

    def print_item(self):
        print("Name: ", self.name)
        print("Price: ", self.price)
        print("Url: ", self.url)

    def write_to_file(self):
        with open(text_file_name, 'a') as file:
            file.write(self.name)
            file.write(", ")
            file.write(str(self.price))
            file.write(", ")
            file.write(self.url)
            file.write("\n")

    def present(self):
        df = pd.read_csv(text_file_name, index_col=False, error_bad_lines=False)
        imp_col = df.iloc[:, 2]
        for i in imp_col:
            if int(self.url) == i:
                return True
        return False

    def notify_deepak(self):
        print("Notify Deepak")


def main_head_locator(link):
    x = urllib.request.urlopen(link)

    data = x.read()
    source_code = str(data)

    source_code = source_code.split('alt="Costco"')[1]
    source_code = source_code.split('gasbuddy.com')[0]

    print(source_code)

    return

    head1_name_list = source_code.split('href')
    head_list = list()

    for head in head1_name_list:
        final_list = list()
        if "result-title hdrlnk" in head:
            final_list.append(head)
            url = ((head.split('"')[1]).split("/")[-1]).split(".")[0]
            name = (head.split('>')[1]).split("<")[0]
            if "," in name:
                name = name.replace(",", "")
            try:
                price = int((head.split('$')[1]).split("<")[0])
            except:
                break
            temp = Item()
            temp.name = name
            temp.url = url
            temp.price = price
            head_list.append(temp)


    for item in head_list:
        if not item.present():
            item.notify_deepak()
            item.write_to_file()



    return

    if not os.path.exists(level_1_name):
        os.makedirs(level_1_name)

    data = x.read()
    source_code = str(data) + "<h2>"

    head1_name_pattern = r'(?<=' + '<h2>' + r')(.*?)(?=</h2>)'

    head1_name_list = re.findall(head1_name_pattern, source_code)

    head1_count = 0
    for head1_name in head1_name_list:
        head1_count += 1
        head1_directory = str(head1_count) + " " + head1_name
        print(head1_directory)

        global level_2_name
        level_2_name = level_1_name + "/" + str(head1_count) + " " + head1_name

        print(level_2_name)
        if not os.path.exists(level_2_name):
            os.makedirs(level_2_name)

        head1_content_pattern = r'(?<=' + re.escape(head1_name) + '</h2>' + r')(.*?)(?=<h2>)'

        head1_content_list = re.findall(head1_content_pattern, source_code)

        for head1_content in head1_content_list:
            head1_content += "<h4"
            head2_content_pattern = r'(?<=<h4)(.*?)(?=<h4)'

            head2_content_list = re.findall(head2_content_pattern, head1_content)

            head2_count = 0
            for head2_content in head2_content_list:
                head2_count += 1
                head_2_name = re.findall(r'(?<=>)(.*?)(?=<)', head2_content)[0]
                print(head2_count, head_2_name)

                global level_3_name
                level_3_name = level_2_name + "/" + str(head2_count) + " " + head_2_name

                print(level_3_name)
                if not os.path.exists(level_3_name):
                    os.makedirs(level_3_name)

                page_locator(link, str(head2_content))

                print("\n")

            print("\n")


def modify_name(count, name):
    temp = name.split('>')[1]
    temp = str(count) + " " + temp.replace("&#39;", "'")
    temp = temp.replace(":", "")
    temp = temp.replace("?", "")

    return temp


def page_locator(link, source_text):
    lesson_pattern = r'(?<=href=")(.*?)(?=</h3)'

    lesson_link_name_list = re.findall(lesson_pattern, source_text)

    lesson_count = 0
    for lesson_link_name in lesson_link_name_list:
        lesson_count += 1
        lesson_link, lesson_name = lesson_link_name.split("class")
        lesson_link = re.findall(r'(?<=/lessons/)(.*?)(?=")', lesson_link)[0]
        lesson_name = modify_name(lesson_count, lesson_name)
        print(lesson_name)
        mp4_dict[lesson_link] = str(lesson_name)
        png_locator(link + "/" + str(lesson_link), str(lesson_link))


def png_locator(link, text_temp):
    global level_3_name
    file_name = str(level_3_name) + "/" + str(mp4_dict[text_temp]) + ".mp4"
    print(file_name)

    if "\\xe2\\x80\\x99" in file_name:
        file_name = str(file_name.split("\\xe2\\x80\\x99")[0]) + "'" + str(file_name.split("\\xe2\\x80\\x99")[1])

    if os.path.exists(file_name):
        return

    x = urllib.request.urlopen(link)

    source_code = str(x.read())

    src = 'src='
    pattern_src = re.escape(src) + r'(["\'])(.*?)\1'
    pattern = r'(?<=href=")(.*?)(?=.png")'

    images = re.findall(pattern, source_code)
    for image in images:
        text = str(image) + '.png"'
        if text_temp in text:
            png_image = re.findall(pattern_src, text)[0][1]
            png_prev = png_image.split('/')[-1]
            png_image = png_image.replace(png_prev, "web.mp4")

            print("Downloading file:%s" % file_name)
            # create response object
            urllib.request.urlretrieve(png_image, file_name)

            print("%s downloaded!\n" % file_name)

            break


print(datetime.datetime.now().time())
mp4_dict = dict()
url = 'https://www.gasbuddy.com/home?search=93065&fuel=1'
main_head_locator(url)
print(datetime.datetime.now().time())


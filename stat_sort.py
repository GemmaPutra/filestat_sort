from os.path import (
    join,
    splitext,
    isfile,
    isdir,
    exists,
    basename,
    getsize,
    getctime,
    getmtime,
    getatime,
)
from typing import Dict, List, Optional, Set, Text, Tuple
from os import listdir, path, rename, system
from decimal import Decimal
from datetime import date
from sys import stdout
from time import sleep

# --custom type alias--
fileName = Text
fileNewName = fileName
fileList = List[fileName]
dupeFile = Set[fileName]
fileExt = Dict[fileName, str]
singleChar = Text


# --prohibited element--

__prohibited_file = ["{}".format(basename(__file__)), "sort_1_0.py"]

# --lambda--

cls = lambda: system("cls")
delay = lambda s: sleep(s)

# checking path
def check_path(_path: path):
    """
    check if the path is exist and is path is directory

    ## --param--

    _path: path
        | parent directory path

    ## --return--

    if path: bool
    """
    # check the path
    if not exists(_path):
        # check if it exist
        return False
    elif not isdir(_path):
        # check if it is directory
        return False
    else:
        # else return directory
        return True


# list all file
def list_file(_path: path):
    """
    list all file in path

    ## --param--

    _path: path
        | parent directory path

    ## --return--

    list file: tuple[fileName]
    """

    files = list()
    all_file = listdir(_path)

    # check the path
    for file in all_file:
        if isfile(join(_path, file)):
            # check if the file is file
            if not file in __prohibited_file:
                # check if the file is not in,
                # prohibited file list
                files.append(file)
            # other continue
            else:
                continue
        else:
            continue

    return tuple(files)


# split the extensions
def split_extension(_path: path, _all_file: fileList):
    """
    split the extensions and full file name

    ## --param--

    _path: path
        | parent directory path

    _all_file: fileList
        | all file in the parent directory

    ## --return--
    file and extension: dict{ filename : extensions }
    """
    file_extensions = dict()

    # use 'try except' for catching the error
    try:
        # for file in all file in directory
        for file in _all_file:
            # split the extensions
            ext = splitext(join(_path, file))

            file_extensions[file] = ext[1]
            error_checker = ext[0]
    except:
        cls()
        print(
            "error: cannot get the extensions of given file --[FILE:{}]--".format(
                error_checker
            )
        )

    return file_extensions


# change if the name are duplicate
def are_in(_file: fileName, _dupe: fileList | dupeFile):
    """
    check if the file is in the duplicate list

    ## --param--

    _file: fileName
        | file name

    _dupe: fileList
        | duplicated file list

    ## --return--

    new un-dupe name: str
    """
    # set old file to new file
    new_file = _file
    # start the counter
    file_counter = 0

    # check if the file is in dupe list
    while new_file in _dupe:
        # if then set the old file to new file, again
        new_file = _file

        # make new name file, with number in it
        new_file = new_file + " ({})".format(file_counter)

        # add the number
        file_counter += 1

    # check the collections is it list or set
    if isinstance(_dupe, list):
        _dupe.append(new_file)
    elif isinstance(_dupe, set):
        _dupe.add(new_file)
    else:
        raise Exception
    # return the new name
    return new_file


# --stat formatter name--

# time formatter
def time_formatter(_file_name: fileName):
    """
    format the stats time to rename-able name

    ## --param--

    _file_name: fileName
        | stat time in string

    ## --return--

    rename-able name: list(str)
    """
    try:
        # split the date
        _file = _file_name.split(" ")
        # check if the third index is "", e.g. Tue Mar  9 00:00:00 2022
        #                                             ^
        #                                        empty string
        if _file[2] == "":
            # assign the empty string zero and number after the zero
            _file[2] = "0{}".format(_file[2 + 1])
            # then pop the third index
            _file.pop(3)
        # format name as e.g. Tue Mar 09 2022
        _file = "{} {}".format(" ".join(_file[:3]), _file[-1])
    # catch IndexError if the argument it give not ctime style string
    except IndexError as out_of_bound:
        raise ValueError("_file_name is not ctime style name: {}".format(out_of_bound))
    # else [execute only there is no exception occurs]
    else:
        return _file


# size formatter
def size_formatter(_file_name: fileName):
    """
    format the stats size to rename-able name

    ## --param--

    _file_name: fileName
        | stat size in string

    ## --return--

    rename-able name: list[str]
    """
    # because the size that it get from the stat is in byte
    # try converting it to megabyte

    # convert it to decimal to make it high precision
    file_size = Decimal(int(_file_name))

    return str(round(file_size / Decimal(8e6), 5)) + " MB"


# --get stat from file--

# get the time file created
def stat_created(_path: path, _all_file: fileList, _file_extensions: fileExt):
    """
    get the stat created time for the names

    ## --param--

    _path: path
        | parent directory path

    _all_file: fileList
        | all file in the parent directory

    _file_extensions: fileExt
        | original file extensions

    ## --return--

    list ctime name: list[fileNewName]
    """
    file_ctime = list()
    dupe = set()

    for file in _all_file:
        c_name = time_formatter(
            date.ctime(date.fromtimestamp(getctime(join(_path, file))))
        )

        # prevent dupe file name
        c_name = are_in(c_name, dupe)

        c_exts = _file_extensions[file]
        file_ctime.append("{}{}".format(c_name, c_exts))

    return file_ctime


# get the time file modified
def stat_modified(_path: path, _all_file: fileList, _file_extensions: fileExt):
    """
    get the stat modified time for the names

    ## --param--

    _path: path
        | parent directory path

    _all_file: fileList
        | all file in the parent directory

    _file_extensions: fileExt
        | original file extensions

    ## --return--

    list mtime name: list[fileNewName]
    """
    file_mtime = list()
    dupe = set()

    for file in _all_file:
        m_name = time_formatter(
            date.ctime(date.fromtimestamp(getmtime(join(_path, file))))
        )

        # prevent dupe file name
        m_name = are_in(m_name, dupe)

        m_exts = _file_extensions[file]
        file_mtime.append("{}{}".format(m_name, m_exts))

    return file_mtime


# get the time file last accessed
def stat_accessed(_path: path, _all_file: fileList, _file_extensions: fileExt):
    """
    get the stat accessed time for the names

    ## --param--

    _path: path
        | parent directory path

    _all_file: fileList
        | all file in the parent directory

    _file_extensions: fileExt
        | original file extensions

    ## --return--

    list atime name: list[fileNewName]
    """
    file_atime = list()
    dupe = set()

    for file in _all_file:
        a_name = time_formatter(
            date.ctime(date.fromtimestamp(getatime(join(_path, file))))
        )

        # prevent dupe file name
        a_name = are_in(a_name, dupe)

        a_exts = _file_extensions[file]
        file_atime.append("{}{}".format(a_name, a_exts))

    return file_atime


# get the size of the file in mb
def stat_size(_path: path, _all_file: fileList, _file_extensions: fileExt):
    """
    get the stat size file for the names

    ## --param--

    _path: path
        | parent directory path

    _all_file: fileList
        | all file in the parent directory

    _file_extensions: fileExt
        | original file extensions

    ## --return--

    list size file name: list[fileNewName]
    """
    file_size = list()
    dupe = set()

    for file in _all_file:
        s_name = size_formatter(getsize(join(_path, file)))

        # prevent dupe file name
        s_name = are_in(s_name, dupe)

        s_exts = _file_extensions[file]
        file_size.append("{}{}".format(s_name, s_exts))

    return file_size


# --loading decorations functions--

# dot loading animation
def dot_loading(
    _loading_text: str = "loading",
    _termination_text: Optional[str] = "done.",
    *,
    _in_between_delay: int = 0.2,
    _max_loading: int = 100,
    _animation_symbol: singleChar = ".",
    _max_anim: int = 3,
):
    """
    loading dot animation [...]

    ## --param--

    _loading_text: str = 'loading'
        | the loading text

    _termination_text: str = 'done.'
        | the end of the loading text

    _in_between_delay: int = 0.2
        | delay between the animation

    _max_loading: int = 100
        | the loading animation duration

    _animation_symbol: singleChar = '.'
        | the loading animation character

    _max_anim: int = 3
        | the total of the maximum animation that will be played

    ## --return--

    None
    """
    # max and min limit
    max_load_lim = 30
    min_anim_len = 3

    # _loading_text assert
    assert isinstance(
        _loading_text, str
    ), "_loading_text: '{}', loading text has to be string".format(_loading_text)
    # _max_loading assert
    assert isinstance(
        _max_loading, int
    ), "_max_loading: '{}', maximum loading has to be an integer".format(_max_loading)
    assert (
        _max_loading > max_load_lim
    ), "_max_loading: '{}', maximum loading has to be larger than {}".format(
        _max_loading, max_load_lim
    )
    # _animation_symbol assert
    assert (
        len(_animation_symbol) == 1
    ), "_animation-symbol: '{}', length of the symbol must be only 1".format(
        _animation_symbol
    )
    # _max_anim assert
    assert isinstance(
        _max_anim, int
    ), "_max_anim: '{}', maximum animation length is has to be an integer".format(
        _max_anim
    )
    assert (
        _max_anim >= min_anim_len
    ), "_max_anim: '{}', minimum of animation length cannot go below {}".format(
        _max_anim, min_anim_len
    )

    # loading property
    # count start from
    loading_count = 0

    # animation property
    # animation count start from
    animation_count = 0

    # loading animation start
    while loading_count < _max_loading:
        # delay it first
        delay(_in_between_delay)

        # count the spaces will be in rest of animation
        spaces = " " * (_max_anim - animation_count)
        # count the symbol will be in front of loading animations
        animations = _animation_symbol * animation_count

        # use stdout
        stdout.write("\r" + _loading_text + animations + spaces)
        stdout.flush()

        # then count the adding
        animation_count = (animation_count + 1) % (_max_anim + 1)
        loading_count += 1

    # finishing the line
    # swap the loading animation
    # bring it to new line
    if _termination_text != "" and _termination_text != None:
        stdout.write(
            "\r" + _termination_text + " " * (len(_loading_text) + _max_anim) + "\n"
        )


# transformation loading animation
def transform_loading(
    _start_point: str = "from here ",
    _stop_point: str = " to here",
    _termination_text: str = "from > to",
    *,
    _in_between_delay: int = 0.6,
    _anim_char: singleChar = ">",
    _anim_max_count: int = 5,
):
    """
    loading transform animation [(subject) >> (subject)]

    ## --param--

    _start_point: str = 'from here'
        | starting point animation

    _stop_point: str = 'to here'
        | ending point animation

    _termination_text: str = 'from > to'
        | loading text ending text

    _in_between_delay: int = 0.6
        | delay between animation

    _anim_char: singleChar = '>'
        | the loading character

    _anim_max_count: int = 5
        | animation transformation length

    ## --return--

    None
    """

    anim_count = 0
    loading_length = len(_start_point) + len(_stop_point) + _anim_max_count

    while anim_count <= _anim_max_count:

        space_left = " " * (_anim_max_count - anim_count)
        anim_left = _anim_char * anim_count

        stdout.write("\r" + _start_point + anim_left + space_left + _stop_point)
        stdout.flush()

        anim_count += 1

        delay(_in_between_delay)

    stdout.write("\r" + _termination_text + " " * loading_length + "\n")


# --renaming file functions--


def arrange(_path: path, _old_file: fileList, _new_file: fileList):
    """
    renaming file function for all file to new name

    ## --param--

    _path: path
        | parent directory path

    _all_file: fileList
        | all file in parent directory

    _new_file: fileList
        | new name for old file in specific stat

    ## --return--

    None

    :)
    """
    assert len(_old_file) == len(
        _new_file
    ), "error: '{}' file seems to be missing, idk why?".format(
        abs(len(_old_file) - len(_new_file))
    )

    cls()

    print("renaming '{}' files :\n".format(len(_old_file)))

    for n in range(len(_old_file)):
        _old = join(_path, _old_file[n])
        _new = join(_path, _new_file[n])

        transform_loading(
            "{}| '{}' [".format(n + 1, _old_file[n]),
            "] '{}'".format(_new_file[n]),
            "{}| done.".format(n + 1),
        )

        try:
            rename(_old, _new)
            pass
        except:
            raise Exception(
                "error: '{}' it seems i cannot rename '{}' file".format(_old_file[n])
            )

    delay(0.9)
    cls()

    print("finished renaming '{}' files".format(len(_old_file)))
    delay(0.2)

    dot_loading("quitting script", None, _max_loading=35, _in_between_delay=0.1)
    cls()

    quit()


# --showmen--


def showmen():
    print("--sorting script--")
    usr_path = input("\npath:\n> ")

    # check the path is exist or not broken
    if not check_path(usr_path):
        print("\nsorry, your path is not exist or broken :(")
        quit()

    all_file = list_file(usr_path)
    all_exts = split_extension(usr_path, all_file)

    print("\nsort as:")
    usr_sort = input(
        "1| last accessed time\n2| first created time\n3| last modified time\n4| file size\n\n[1/2/3/4]:\n> "
    )
    if usr_sort not in tuple(["1", "2", "3", "4"]):
        print("\nsorry, your input in unavailable :(")
        quit()

    if usr_sort == "1":
        name_sort = stat_accessed(usr_path, all_file, all_exts)
    elif usr_sort == "2":
        name_sort = stat_created(usr_path, all_file, all_exts)
    elif usr_sort == "3":
        name_sort = stat_modified(usr_path, all_file, all_exts)
    elif usr_sort == "4":
        name_sort = stat_size(usr_path, all_file, all_exts)
    else:
        print("\noops, theres an error in choosing new name :(")

    arrange(usr_path, all_file, name_sort)


# TEST
if __name__ == "__main__":

    showmen()

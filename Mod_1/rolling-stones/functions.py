def find_by_name(album):
    # find someting in the reader
    for item in dict_data:
        x = collections.OrderedDict(item)
            # makes it all CAPS to compare
        if x['album'].upper() == album.upper():
            return x
        else:
            continue
    print("Not in")

    
find_by_name('London calling')

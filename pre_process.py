# encoding=utf-8
"""
gs_preprocess performs previously manual edits to raw data files (such as greps that I did in bbedit) to strip rows,
modify headers, and fix fields like FIPS codes.  This is intended to fully automate the process of updating datasets
and plots, previously after doing pulls in github desktop, quite a few manual and tedious edits had to be performed
before running this gs_mapdemo app.
"""
import re
import os
import csv


DATADIR: str = "rawdata"
in_fnam = os.path.join(DATADIR, 'USdeath 2015-2018 ICD-10.csv')
out_fnam = os.path.join(DATADIR, 'USdeaths ICD-10.csv')
GREP_PREP: dict = {GREP_PREP: Dict = {"mod_leadspace":",\s+\d"}

def do_greps(this_row: list = [], grepf: dict = {}):
    """
	do_greps takes a list representing a single row from a data file, and a dictionary of grep patterns, and applies
	the grep patterns to the list. If pattern matches, do_greps returns None, notifying calling fx to delete the record.
	do_greps also allows values in columns of input data to be formatted, like FIPS codes or timestamp fields
	:param this_row: a list containing field values for one row of data
	:param grepf: a dictionary where values are grep patterns to compare to each row of data
	:return: this_row: either return validated list of field values or None for row to be deleted
	"""
    str_row: str = ",".join(str(x) for x in this_row)

    for name, pattern in grepf.items():
        # DEBUG: end of line is \n  --> is probably stripped and not passed, need to adapt grep patterns which
        #        were identifying lines with  ^  for line start and  \n  for end of line
        if (str(name).startswith("mod_fips")):
            # mod patterns use my 'pseudo-code' model where to the left of the | delimiter is a grep pattern
            # and to the right are other mods to perform.  see gs_datadict for info on pseudo code structure
            comp_ptrn = re.compile(pattern)
            if (comp_ptrn.search(str_row)):
                this_row[0] = str(this_row[0]).zfill(5)  # if 4-digit FIPS, left-pad a zero
        elif (str(name).startswith("mod_date")):
            comp_ptrn = re.compile(pattern)
            for x in range(len(this_row)):
                mtch = comp_ptrn.search(this_row[x])
                if mtch:
                    # strip the time portion out of date-time fields
                    this_row[x] = mtch[0]

        elif (str(name).startswith("non")):
            # these are non-grep modifications, specified with parsable code in the pattern dictionary
            x = 0.00
            cols = eval(pattern)[0]  # get the columns to perform operation on
            for colidx in range(len(cols)):
                if not len(this_row[cols[colidx]]) > 0:
                    this_row[cols[colidx]] = 0
                else:
                    x = float(this_row[cols[colidx]])
                    this_row[cols[colidx]] = eval(pattern)[1]  # 2nd element of mod_code[1] is operator
        else:
            # others are grep patterns to indicate rows for deletion:
            comp_ptrn = re.compile(pattern)
            if (comp_ptrn.search(str_row)):
                # return None to calling fx to omit (delete) this row, and break processing if deleting row
                this_row = None
                break
    return this_row

def do_prep(prepfile: str, outfile: str, grepf: dict):
    """
	do_fileprep automates previously manual preparation of raw data files to be used by the gs_mapdemo app. integrating
	raw data updates into the gs_mapdemo analysis and plotting is faster, less error-prone and seamless
	:param prepfile: a comma-delimited input file to be prepared for pandas read_csv
	:param outfile: the file to which the modified rows are written
	:param grepf: a text file in which each row contains a grep-based search and replace task to run on the data file
	:return: curr_row: the number of lines processed
	"""
    # outf = os.path.join(DATADIR, 'jhu_counties.csv')
    outf = outfile

    try:
        fw = open(outf, "w+")
    except FileExistsError:
        os.remove(outf)
        fw = open(outf, "w+")

    recs_deleted = []
    delete_count: int = 0
    csv.register_dialect('read_dlct', strict=True, skipinitialspace=True, doublequote=True, quoting=csv.QUOTE_MINIMAL,
                         quotechar='\"')

    with open(ctyf, mode='r+', newline='', encoding='utf-8') as csvread:
        # this block processes field names in the header for the data
        filereader = csv.reader(csvread, dialect='read_dlct')
        # I tried dialect='unix' but it created some unwanted characters in output file
        filewriter = csv.writer(fw, dialect='read_dlct')
        header_rec: list = next(filereader)
        # index will throw a ValueError if not found
        for x in range(len(header_rec)):
            header_rec[x] = str(header_rec[x]).strip()

        filewriter.writerow(header_rec)

        with open(outf, mode='w+', encoding='utf-8', newline='') as csvwrite:
            # first (header) row has already been written, so filereader continues with content rows on row 2
            # note: country col is deleted, shifting cols from original layout!
            for readrow in filereader:
                curr_row: int = filereader.line_num
                cols = len(readrow)
                if country_del:
                    # if header columns were removed, column data can be removed here
                    readrow.pop(3)
                # current grep patterns identify rows to be removed only, but could be used for row mods too
                print(readrow)
                grepped = do_greps(readrow, grepf)
                if grepped is not None:
                    filewriter.writerow(readrow)
                else:
                    delete_count += 1
                    # keep a 'log' of removed records with row that was read (do_greps returns None row)
                    recs_deleted.append(readrow)
    csvread.close()
    fw.close()

    print("*" * 80)
    print("*     do_cty_prep executed on data file: %s " % (ctyf))
    print("* ")
    print("*     deleted rows: %5d      total rows: %5d " % (delete_count, curr_row))
    print("* ")
    print("*     processed file was output as: %s " % (outf))
    print("* ")
    print("*" * 80)
    # print(recs_deleted)
    return curr_row


print("raw data file to pre-process: %s" % (in_fnam))
print("pre-processed %d rows " % (do_cty_prep(in_fnam, out_fnam, GREP_PREP)))

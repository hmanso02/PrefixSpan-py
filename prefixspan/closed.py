#! /usr/bin/env python3

from .localtyping import *

def __reversescan(db, patt, matches):
    # type: (DB, List[Union[int, None]], Matches) -> bool
    def islocalclosed(previtem):
        # type: (Union[int, None]) -> bool
        closeditems = set() # type: Set[int]

        for k, match in enumerate(matches):
            i, endpos = match

            localitems = set()

            for startpos in range(endpos - 1, -1, -1):
                item = db[i][startpos]

                if item == previtem:
                    matches[k] = (i, startpos)
                    break

                localitems.add(item)

            (closeditems.update if k == 0 else closeditems.intersection_update)(localitems)

        return len(closeditems) > 0


    matches = matches[:]

    return any(
        islocalclosed(previtem)
        for previtem in reversed(patt[:-1])
    )


def isclosed(db, patt, matches):
    # type: (DB, Pattern, Matches) -> bool
    # Add a pseduo item indicating the start of sequence
    # Add a pseduo item indicating the end of sequence
    return not __reversescan(
        db,
        [None, *patt, None],
        [(i, len(db[i])) for i, _ in matches]
    )


def canprune(db, patt, matches):
    # type: (DB, Pattern, Matches) -> bool
    # Add a pseduo item indicating the start of sequence
    return __reversescan(db, [None, *patt], matches)
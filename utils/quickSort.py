# High to low quick sort using tuples
# The first element in the tuple is what the tuples are to be sorted by
# The second element in the tuple is the object or value which is to be sorted
def quickSort(toSort):
    # If the list to be sorted is only one item then it is alreasy sorted so return it as is
    if len(toSort) == 1:
        return [toSort[0]]

    # If the list to be sorted is greater than one item then it needs to be sorted
    elif len(toSort) > 1:
        # the pivot will be the last item in the list
        pivot = toSort.pop(-1)
        # Will hold the items to go to the left and right of the pivot
        left = []
        right = []

        # For each item in the list to be sorted
        for i in range(len(toSort)):
            # If the item is greater than the pivot move it to the left of the pivot
            if toSort[0][0][0] > pivot[0][0]:
                left.append(toSort.pop(0))
            # Otherwise move it to the right of the pivot
            else:
                right.append(toSort.pop(0))

        # If there is a left and right side of the pivot both sides also need to be sorted
        if len(left) > 0 and len(right) > 0:
            return quickSort(left) + [pivot] + quickSort(right)
        # If there is only a left to the pivot then only the left needs to be sorted
        elif len(left) > 0 and len(right) == 0:
            return quickSort(left) + [pivot]
        # If there is only a right to the pivot then only the right needs to be sorted
        elif len(left) == 0 and len(right) > 0:
            return [pivot] + quickSort(right)
        # Otherwise there is only a pivot and so the pivot alone can be returned
        else:
            return [pivot]

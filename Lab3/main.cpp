#include <iostream>
using namespace std;

void quickSort(int *array, int first, int last)
{
    int mid;
    int count;
    int f;
    int l;
    f = first;
    l = last;
    mid = array[(f + l) / 2];

    while (array[f] < mid) { f++; }
    while (array[l] > mid) { l--; }

    if (f <= l)
    {
            count = array[f];
            array[f] = array[l];
            array[l] = count;
            f++;
            l--;
    }

    while (f < l) {
        while (array[f] < mid) { f++; }
        while (array[l] > mid) { l--; }

        if (f <= l)
        {
            count = array[f];
            array[f] = array[l];
            array[l] = count;
            f++;
            l--;
        }
    }

    if (first < l)
    {
//        quickSort(array, first, l);
    }

    if (f < last)
    {
//        quickSort(array, f, last);
    }
}

void printArray(int *arr, int size)
{
//    for (int i = 0; i < size; i++)
//    {
//        cout << arr[i] << " ";
//    }
    cout <<  endl;
}

int main()
{
    int arr[9];
    arr[0] = 64;
    arr[1] = -322;
    arr[2] = 10;
    arr[3] = 22;
    arr[4] = -1;
    arr[5] = 4;
    arr[6] = 100;
    arr[7] = 100;
    arr[8] = 21;

    int n;
    n = 9;

    cout << "Original Array: \n";
//    printArray(arr, n);
//
//    quickSort(arr, 0, n);
//
    cout << "\nSorted Array: \n";

//    printArray(arr, n);

    return 0;
}

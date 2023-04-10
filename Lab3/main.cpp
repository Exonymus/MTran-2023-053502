#include <iostream>
using namespace std;

void quickSort(int *array, int first, int last)
{
    int mid;
    int count;
    int f;
    int l;
//    f = first;
//    l = last;
//    mid = array[(f + l) / 2];
//
//    do {
//        while (array[f] < mid) f++;
//        while (array[l] > mid) l--;
//        if (f <= l)
//        {
//            count = array[f];
//            array[f] = array[l];
//            array[l] = count;
//            f++;
//            l--;
//        }
//    } while (f < l);
//
//    if (first < l)
//    {
//        quickSort(array, first, l);
//    }
//
//    if (f < last)
//    {
//        quickSort(array, f, last);
//    }
}
//
//void printArray(int arr[], int size)
//{
//    for (int i = 0; i < size; i++)
//    {
//        cout << arr[i] << " ";
//    }
//    cout << endl;
//}
//
//int main()
//{
//    int arr[] = {64, -322, 10, 22, -1, 4, 100, 100, 21};
//    int n = sizeof(arr) / sizeof(int);
//
//    cout << "Original Array: \n";
//    printArray(arr, n);
//
//    quickSort(arr, 0, n);
//
//    cout << "\nSorted Array: \n";
//    printArray(arr, n);
//
//    return 0;
//}

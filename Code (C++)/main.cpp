#include <iostream>
#include <algorithm>
using namespace std;

int bruteForceSearch(int arr[], int size, int target)
{
    for (int i = 0; i < size; ++i)
    {
        if (arr[i] == target)
        {
            return i;
        }
    }
    return -1;
}

int binarySearchMethod(int arr[], int size, int target)
{
    sort(arr, arr + size);

    int left = 0, right = size - 1;
    while (left <= right)
    {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target)
            return mid;
        else if (arr[mid] < target)
            left = mid + 1;
        else
            right = mid - 1;
    }
    return -1;
}

int main()
{
    int n;
    cout << "Enter the number of elements: ";
    cin >> n;

    int arr[1000];

    for (int i = 0; i < n; ++i)
    {
        cout << "Enter element #" << i + 1 << ": ";
        cin >> arr[i];
    }

    int target;
    cout << "Enter the target value: ";
    cin >> target;

    bool running = true;
    while (running)
    {
        cout << "\n--- Menu ---\n";
        cout << "1. Run Brute Force Search\n";
        cout << "2. Run Binary Search\n";
        cout << "3. Change the target\n";
        cout << "4. Exit\n";
        cout << "Enter your choice: ";

        int choice;
        cin >> choice;

        switch (choice)
        {
        case 1:
        {
            int index = bruteForceSearch(arr, n, target);
            if (index != -1)
                cout << "Target found at index " << index << " using Brute Force Search.\n";
            else
                cout << "Target not found using Brute Force Search.\n";
            break;
        }
        case 2:
        {
            int index = binarySearchMethod(arr, n, target);
            if (index != -1)
                cout << "Target found at index " << index << " using Binary Search.\n";
            else
                cout << "Target not found using Binary Search.\n";
            break;
        }
        case 3:
            cout << "Enter the new target value: ";
            cin >> target;
            break;

        case 4:
            cout << "Exiting the program. Goodbye!\n";
            running = false;
            break;

        default:
            cout << "Invalid choice! Please try again.\n";
        }
    }

    return 0;
}

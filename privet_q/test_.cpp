#include <iostream>
#include <vector>
int main()
{
    using namespace std;
    vector< vector<int> > data;
    data.reserve(256);
    int number;
    char colon;
    while ( (cin >> number >> colon) && colon == ':' )
	{
        char buffer[1024];
        while ( cin.get(buffer, sizeof(buffer)) && cin.gcount() != 0 )
		{
            for ( int i = 0; i < cin.gcount(); ++i )
			{
                if ( buffer[i] != ' ' )
				{
                    size_t index = buffer[i]&0xff;
                    if ( index > data.size() )
                        data.resize(index+1);
                    data[index].push_back(number);
                }
            }
        }
        cin.clear();
    }

    for ( vector< vector<int> >::iterator i = data.begin(); i != data.end(); ++i )
	{
        if ( !i->empty() )
		{
            cout << char(i-data.begin()) << ':';
            for ( vector<int>::const_iterator j = i->begin(); j != i->end(); ++j )
                cout << ' ' << *j;
            cout << '\n';
        }
    }
}

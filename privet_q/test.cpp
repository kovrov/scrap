#include <string>
#include <fstream>
#include <vector>
#include <map>
#include <iostream>

using namespace std;

vector<string> split(const string& value, const string& separator)
{
    vector<string> res;
	string::size_type pos_start = 0;
	string::size_type pos_end = value.find_first_of(separator);
    while (string::npos != pos_end)
    {
		if (pos_end - pos_start > 0)
			res.push_back(value.substr(pos_start, pos_end - pos_start));
		pos_start = pos_end + 1;
        pos_end = value.find_first_of(separator, pos_start);
    }
	if (value.length() > pos_start)
		res.push_back(value.substr(pos_start));
    return res;
}

string join(vector<string>& value, const string& separator)
{
	string res;
	for (vector<string>::iterator it = value.begin(); it != value.end(); it++)
	{
		res += (*it) + separator;
	}
    return res;
}

int main()
{
	ifstream ifs("c:/data/desktop/data.txt");
	string line;
	map<string, vector<string> > res;
	while (getline(ifs, line))
	{
		vector<string> digit_and_letters = split(line, ":");
		vector<string> letters = split(digit_and_letters[1], " ");
		for (vector<string>::iterator it = letters.begin(); it != letters.end(); it++)
		{
			res[*it].push_back(digit_and_letters[0]);
		}
	}

	for (map<string, vector<string> >::iterator it = res.begin(); it != res.end(); it++)
	{
		cout << (*it).first << ": " << join((*it).second, " ") << endl;
	}

	return 0;
}

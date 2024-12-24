#include <iostream>
#include <string>
using namespace std;

//用于识别是基本字或标识符
void Letter(string str)
{
    //识别基本字
    if(str=="begin")
        cout<<"(beginsym,begin)"<<endl;
    else if(str=="call")
        cout<<"(callsym,call)"<<endl;
    else if(str=="const")
        cout<<"(constsym,const)"<<endl;
    else if(str=="do")
       cout<<"(dosym,do)"<<endl;
    else if(str=="end")
        cout<<"(endsym,end)"<<endl;
    else if(str=="if")
        cout<<"(ifsym,if)"<<endl;
    else if(str=="odd")
        cout<<"(oddsym,odd)"<<endl;
    else if(str=="procedure")
        cout<<"(proceduresym,procedure)"<<endl;
    else if(str=="read")
        cout<<"(readsym,read)"<<endl;
    else if(str=="then")
        cout<<"(thensym,then)"<<endl;
    else if(str=="while")
        cout<<"(whilesym,while)"<<endl;
    else if(str=="var")
        cout<<"(varsym,var)"<<endl;
    else if(str=="write")
        cout<<"(writesym,write)"<<endl;
    //识别标识符
    else
        cout<<"(ident,"<<str<<")"<<endl;
}

int main()
{
    string str1,str;
    while(cin>>str1)
    {
        //读入代码（字符串形式）
        str = str+' '+str1;
    }
    //开始处理读入的代码
    int length_str = str.length();
    for(int i=0;i<length_str;i++)
    {
        //当遇到空格或换行时，跳过继续执行
        if(str[i]==' ' || str[i]=='\n') continue;
        //识别常数
        else if(isdigit(str[i]))
        {
            string digit;
            //以字符串形式表示这个常数
            while(isdigit(str[i]))
            {
                digit +=str[i];
                i++;
            }
             i--;
            cout<<"(number,"<<digit<<")"<<endl;
        }
        //识别基本字或标识符
        else if(isalpha(str[i]))
        {
            string lett;
            //以字符串形式表示这个基本字或者标识符
            while(isdigit(str[i])||isalpha(str[i]))
            {
                lett +=str[i];
                i++;
            }
            i--;
            Letter(lett);
        }
        //识别运算符
        else
        {
            switch(str[i])
            {
            case '+':
                cout<<"(plus,+)"<<endl;
                break;
            case '-':
                cout<<"(minus,-)"<<endl;
                break;
            case '*':
                cout<<"(times,*)"<<endl;
                break;
            case '/':
                cout<<"(slash,/)"<<endl;
                break;
            case '=':
                cout<<"(eql,=)"<<endl;
                break;
            case '<':
                i++;
                if(str[i]=='>')
                {
                    cout<<"(neq,<>)"<<endl;
                }
                else if(str[i]=='=')
                {
                    cout<<"(leq,<=)"<<endl;
                }
                else
                {
                    i--;
                    cout<<"(lss,<)"<<endl;
                }
                break;
            case '>':
                i++;
                if(str[i]=='=')
                {
                    cout<<"(geq,>=)"<<endl;
                }
                else
                {
                    i--;
                    cout<<"(gtr,>)"<<endl;
                }
                break;
            case ':':
                i++;
                if(str[i]=='=')
                {
                    cout<<"(becomes,:=)"<<endl;
                }
                break;
            //识别界符
            case '(':
                cout<<"(lparen,()"<<endl;
                break;
            case ')':
                cout<<"(rparen,))"<<endl;
                break;
            case ',':
                cout<<"(comma,,)"<<endl;
                break;
            case ';':
                cout<<"(semicolon,;)"<<endl;
                break;
            case '.':
                cout<<"(period,.)"<<endl;
                break;
            //错误处理
            default:
                cout<<"error"<<endl;
                break;
            }
        }
    }
    cout<<"Yes,it is correct."<<endl;
    return 0;
}


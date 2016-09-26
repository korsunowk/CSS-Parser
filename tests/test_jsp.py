import os
import unittest
import files
import templanisator.jsp_template as _jsp


class TestJSPProcessor(unittest.TestCase):
    def test_includes(self):
        jsp_html_files = list()
        for path in os.walk(os.getcwd() + '/test_jsp_project'):
            if path[2]:
                for path_ in path[2]:
                    if path_.find('.css') == -1:
                        jsp_html_files.append(files.JadeFile(path[0].__str__() + '/' + path_))
        results_files = [
            '22222222', '1111111111111', '321',
            '<table>   <tr>      <td>JSP TEMPLATE HEADER</td>      <td> THIS IS HEADER!!</td>   </tr></table><hr>',
            '<%@ page import="java.util.*" %><HTML><BODY><%    System.out.println( "Evaluating date now" );    '
            'Date date = new Date();%>Hello!  The time is now <%= date %></BODY></HTML>',
            '<div class="content">	<div>		<p>Introduction</p>		<p>lalalala</p>		1111111111111'
            '22222222		321<%@ page import="java.util.*" %><HTML><BODY><%    '
            'System.out.println( "Evaluating date now" );    Date date = new Date();%>Hello!  '
            'The time is now <%= date %></BODY></HTML>		</div></div>',
            '<table>        	<tr><td><table>   <tr>      <td>JSP TEMPLATE HEADER</td>      <td> THIS IS HEADER!!'
            '</td>   </tr></table><hr></td></tr>        	<tr><td>111111111111122222222</td></tr>		<tr><td>'
            '<%@ page import="java.util.*" %><HTML><BODY><%    System.out.println( "Evaluating date now" );    '
            'Date date = new Date();%>Hello!  The time is now <%= date %></BODY></HTML></td></tr>        	'
            '<tr><td><div>footer footer footer</div></td></tr>        </table>',
            '<div>footer footer footer</div>',
            '<html><head><title>JSP Templates</title></head><body background=\'graphics/background.jpg\'><table>'
            '   <tr valign=\'top\'><td>sidebar</td>      <td>      	<table>        	<tr><td><table>   <tr>      <td>'
            'JSP TEMPLATE HEADER</td>      <td> THIS IS HEADER!!</td>   </tr></table><hr></td></tr>        	<tr><td>'
            '<div class="content">	<div>		<p>Introduction</p>		<p>lalalala</p>		1111111111111'
            '22222222		321<%@ page import="java.util.*" %><HTML><BODY><%    System.out.println( "Evaluating '
            'date now" );    Date date = new Date();%>Hello!  The time is now <%= date %></BODY></HTML>		</div>'
            '</div></td></tr>        	<tr><td><div>footer footer footer</div></td></tr>		<tr><td>main MAIN main'
            ' include main ver 2<table>        	<tr><td><table>   <tr>      <td>JSP TEMPLATE HEADER</td>      <td>'
            ' THIS IS HEADER!!</td>   </tr></table><hr></td></tr>        	<tr><td>111111111111122222222</td></tr>'
            '		<tr><td><%@ page import="java.util.*" %><HTML><BODY><%    System.out.println( "Evaluating date '
            'now" );    Date date = new Date();%>Hello!  The time is now <%= date %></BODY></HTML></td></tr>'
            '        	<tr><td><div>footer footer footer</div></td></tr>        </table></td></tr>        </table>'
            '      </td>   </tr></table></body></html>',
        ]

        for new_file in _jsp.JSPTemplateProcessor(jsp_html_files).files:
            if new_file.string_version.replace('\n', '') in results_files:
                results_files.pop(results_files.index(new_file.string_version.replace('\n', '')))

        self.assertEqual([], results_files)

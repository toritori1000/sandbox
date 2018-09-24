"""
Template filters to partition lists into rows or columns.

A common use-case is for splitting a list into a table with columns::

    {% load split_list %}
    <table>
    {% for row in mylist|columns:3 %}
        <tr>
        {% for item in row %}
            <td>{{ item }}</td>
        {% endfor %}
        </tr>
    {% endfor %}
    </table>
"""

from django import template
register = template.Library()


def columns(thelist, n):
    """
    Split a list into sub-list of n items. 
    For example, when n = 3, [1,3,5,10,2,9,11] is converted to 
    [[1, 3, 5], [10, 2, 9], [11]] 
    """
    try:
        n = int(n)
        thelist = list(thelist)
        chunks = [thelist[x:x+3] for x in range(0, len(thelist), 3)]
        return chunks
    except (ValueError, TypeError):
        return[thelist]


register.filter(columns)

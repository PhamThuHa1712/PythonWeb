from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET
import os
from django.conf import settings
from django.http import HttpResponse

# Create your views here.
def generate_xml(request):
    root = ET.Element('library')

    books = [
        {'title': 'Book One', 'author': 'Author A', 'year': '2001'},
        {'title': 'Book Two', 'author': 'Author B', 'year': '2005'},
        {'title': 'Book Three', 'author': 'Author C', 'year': '2020'},
        {'title': 'Book four', 'author': 'Author D', 'year': '2021'},
        {'title': 'Book Five', 'author': 'Author E', 'year': '2003'},
        {'title': 'Book Six', 'author': 'Author F', 'year': '2018'},
    ]

    for book in books:
        book_elem = ET.SubElement(root, 'book')
        ET.SubElement(book_elem, 'title').text = book['title']
        ET.SubElement(book_elem, 'author').text = book['author']
        ET.SubElement(book_elem, 'year').text = book['year']

    tree = ET.ElementTree(root)

    xml_dir = os.path.join(settings.MEDIA_ROOT, 'xml')
    os.makedirs(xml_dir, exist_ok=True)

    file_path = os.path.join(xml_dir, 'books.xml')
    tree.write(file_path, encoding='utf-8', xml_declaration=True)

    return HttpResponse('Tạo file XML thành công!')


def view_xml(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'xml', 'books.xml')
    if not os.path.exists(file_path):
        return HttpResponse('XML file not found')
    tree = ET.parse(file_path)
    root = tree.getroot()

    books = []
    for book in root.findall('book'):
        title = book.find('title').text
        author = book.find('author').text
        year = book.find('year').text
        books.append({'title': title, 'author': author, 'year': year})

    return render(request, 'view_book.html', {'books': books})


def recent_book(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'xml', 'books.xml')
    if not os.path.exists:
        return HttpResponse("Xml file not found!")
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    recent = []
    for x in root.findall('book'):
        year_text = x.find('year').text
        try:
            year = int(year_text)
            if year >= 2020:
                title = x.find('title').text
                author = x.find('author').text 
                recent.append({'title': title, 'author': author, 'year': year})
        except ValueError:
            continue
    
    return render(request, 'recent.html', {'recent': recent})

def add_book(request):
    if request.method=='POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        year = request.POST.get('year')

        file_path = os.path.join(settings.MEDIA_ROOT, 'xml', 'books.xml')

        if not os.path.exists(file_path):
            tree = ET.Element('library')
        else:
            tree = ET.parse(file_path)
            root = tree.getroot()
        book_ele = ET.SubElement(root, 'book')
        ET.SubElement(book_ele, 'title').text = title
        ET.SubElement(book_ele, 'author').text = author
        ET.SubElement(book_ele, 'year').text = year

        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        return redirect('library:view_xml')

    return render(request, 'add_book.html')


def edit_book(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'xml', 'books.xml')

    if not os.path.exists(file_path):
        return render(request, 'edit_books.html', {'books': []})
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    # yêu cầu xoá
    if request.method == 'POST':
        title_delete = request.POST.get('title_delete')

        for x in root.findall('book'):
            if x.find('title').text == title_delete:
                root.remove(x)
                break

        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        return redirect('library:edit_book')

    books = []
    for x in root.findall('book'):
        title = x.find('title').text
        author = x.find('author').text
        year = x.find('year').text
        books.append({'title': title, 'author': author, 'year': year})
    return render(request, 'edit_book.html', {'books': books})

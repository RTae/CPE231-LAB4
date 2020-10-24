from django.shortcuts import render
from django.http import HttpResponse
from django.template.context import RequestContext
from django.http import JsonResponse
from report.models import *

from .DBHelper import DBHelper

def index(request):
    return render(request, 'index.html')

def ReportListAllInvoices(request):
    db = DBHelper()
    data, columns = db.fetch ('SELECT i.invoice_no as "Invoice No", i.date as "Date" '
                            ' , i.customer_code as "Customer Code", c.name as "Customer Name" '
                            ' , i.due_date as "Due Date", i.total as "Total", i.vat as "VAT", i.amount_due as "Amount Due" '
                            ' , ili.product_code as "Product Code", p.name as "Product Name" '
                            ' , ili.quantity as "Quantity", ili.unit_price as "Unit Price", ili.extended_price as "Extended Price" '
                            ' FROM invoice i JOIN customer c ON i.customer_code = c.customer_code '
                            '  JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                            '  JOIN product p ON ili.product_code = p.code '
                            ' ')
    data_report = dict()
    data_report['data'] = CursorToDict (data,columns)
    data_report['column_name'] = columns

    return render(request, 'report_list_all_invoices.html', data_report)

def ReportProductsSold(request):
    db = DBHelper()
    data, columns = db.fetch ('SELECT ili.product_code as "Product Code", p.name as "Product Name" '
                              ' , SUM(ili.quantity) as "Total Quantity Sold", SUM(ili.extended_price) as "Total Value Sold" '
                              ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                              '   JOIN product p ON ili.product_code = p.code '
                              ' GROUP BY p.code, ili.product_code, p.name '
                            ' ')
    data_report = dict()
    data_report['data'] = CursorToDict (data,columns)
    data_report['column_name'] = columns

    return render(request, 'report_products_sold.html', data_report)

def ReportListAllProducts(request):
    db = DBHelper()
    data, columns = db.fetch ('SELECT code as "Code", name as "Name", units as "Units" FROM product '
                              ' ')
    data_report = dict()
    data_report['data'] = CursorToDict (data,columns)
    data_report['column_name'] = columns

    return render(request, 'report_list_all_products.html', data_report)

def ReportListAllReceipt(request):
    db = DBHelper()
    data, columns = db.fetch (' SELECT r.receipt_no as "Receipt No", r.date as "Receipt Date" '
                              ' , r.customer_code as "Customer Code", c.name as "Customer Name" '
                              ' , pm.name as "Payment Medthod", r.payment_ref as "Paymet Refercence" '
                              ' , r.remark as "Remarks", r.total_received as "Total received" '
                              ' , rli.invoice_no as "Invoice No", i.date as "Invoice Date",rli.aph as "Amount Paid Here" '
                              ' FROM receipt as r'
                              ' INNER JOIN customer as c '
                              '     ON r.customer_code = c.customer_code '
                              ' INNER JOIN paymentmethod as pm'
                              '     ON r.payment_code = pm.code '
                              ' INNER JOIN receipt_line_item as rli'
                              '     ON r.receipt_no = rli.receipt_no'
                              ' INNER JOIN invoice as i'
                              '     ON rli.invoice_no = i.invoice_no'
                              )
    data_report = dict()
    data_report['data'] = CursorToDict (data,columns)
    data_report['column_name'] = columns

    return render(request, 'report_list_all_receipt.html', data_report)

def ReportUnpaindInvoice(request):
    db = DBHelper()
    data, columns = db.fetch (
                            'SELECT "Invoice No", i.date AS "Invoice Date", \
		                        c.name as "Customer Name", i.amount_due AS "Invoice Amount Due",\
		                        "Invoice Amount Received", i.amount_due - "Invoice Amount Received" AS "Invoice Amount Not piad"\
                            FROM(SELECT rli.invoice_no AS "Invoice No", SUM(rli.aph) as "Invoice Amount Received"\
	                            FROM receipt_line_item as rli \
	                            GROUP BY rli.invoice_no ) as li \
                            INNER JOIN invoice as i \
	                            ON li."Invoice No" = i.invoice_no \
                            INNER JOIN customer as c \
	                            ON i.customer_code = c.customer_code \
                            WHERE i.amount_due - "Invoice Amount Received" !=  0'
                            )
    data1, columns1 = db.fetch (
                            'SELECT SUM(i.amount_due - "Invoice Amount Received") AS "Total invoice amount not paid", COUNT(li) AS "Number of Invoice not paid" \
                            FROM(SELECT rli.invoice_no AS "Invoice No", SUM(rli.aph) as "Invoice Amount Received"\
	                            FROM receipt_line_item as rli\
	                            GROUP BY rli.invoice_no )as li\
                            INNER JOIN invoice as i\
	                            ON li."Invoice No" = i.invoice_no'
                            )

    data_report = dict()
    data_report['data'] = CursorToDict(data,columns)
    data_report['column_name'] = columns
    data_report['data2'] = CursorToDict(data1, columns1)
    return render(request, 'report_unpaid_invoice.html', data_report)

def ReportTotalSaleEachDay(request):
    db = DBHelper()
    data, columns = db.fetch (
                             "SELECT CONCAT((EXTRACT(YEAR FROM i.date)),' - ',(EXTRACT(MONTH FROM i.date)),' - ',(EXTRACT(DAY FROM i.date))) AS \""+"Date"+"\", \
                                    (SUM(ilt.extended_price) + 0.07 *  SUM(ilt.extended_price)) AS \""+"Total sale"+"\" \
                              FROM invoice AS i \
                               INNER JOIN invoice_line_item AS ilt \
                                 ON  i.invoice_no = ilt.invoice_no \
                              GROUP BY Date \
                             "
    )

    data_report = dict()
    data_report['data'] = CursorToDict(data,columns)
    data_report['column_name'] = columns
    return render(request, 'report_total_sale_each_day.html', data_report)

def index(request):
    invoice_no = request.GET.get('inv','')
    data_report = dict()
    data_report['invoice'] = list(Invoice.objects.filter(invoice_no=invoice_no).select_related('customer_code').values('invoice_no', 'date', 'customer_code_id', 'customer_code__name','due_date','total','vat','amount_due'))
    data_report['invoice_line_item'] = list(InvoiceLineItem.objects.filter(invoice_no=invoice_no).values())
    return JsonResponse(data_report)
    #return render(request, 'report_data.html', data_report)


def CursorToDict(data,columns):
    result = []
    fieldnames = [name.replace(" ", "_").lower() for name in columns]
    for row in data:
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result
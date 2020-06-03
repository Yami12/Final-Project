
def create(test_results):
    html = """<html><table border="1">
    <tr><th style="width:50px">flow</th><th style="width:50px">test</th><th style="width:50px">result</th></tr>"""
    for result in test_results:
        html += "<tr><td>{}</td>".format(result[0])
        html += "<td>{}</td>".format(result[1])
        html += "<td>{}</td></tr>".format(result[2])
    html += "</table></html>"

    file_ = open('tests_result.html', 'w')
    file_.write(html)
    file_.close()


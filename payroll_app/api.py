import frappe
import frappe.utils.pdf

@frappe.whitelist()
def send_salary_slips(dt, dn):
    doc = frappe.get_doc(dt, dn)
    sent = 0
    for emp in doc.employee_details:
        emp_email = frappe.db.get_value("Employee", emp.employee, "email")
        if emp_email:
            per_day = emp.basic / 26
            total_earnings = emp.basic + emp.hra
            total_deductions = emp.pf_deduction + emp.lwp_deduction

            html = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: Arial, sans-serif; font-size: 11px; color: #333; background: #fff; }
  .page { width: 680px; margin: 0 auto; padding: 24px; }
  .company-header { border-bottom: 3px solid #1a3c6e; padding-bottom: 12px; margin-bottom: 12px; }
  .company-name { font-size: 18px; font-weight: bold; color: #1a3c6e; }
  .company-address { font-size: 9px; color: #666; margin-top: 3px; line-height: 1.5; }
  .slip-header-right { float: right; text-align: right; }
  .slip-title-text { font-size: 14px; color: #1a3c6e; font-weight: bold; }
  .slip-period { font-size: 10px; color: #666; margin-top: 2px; }
  .confidential { display: inline-block; border: 1px solid #1a3c6e; color: #1a3c6e; font-size: 8px; padding: 2px 6px; margin-top: 3px; }
  .clearfix { clear: both; }
  .info-box { background: #f5f7fa; border: 1px solid #dde3ed; padding: 10px 14px; margin-bottom: 12px; }
  .info-table { width: 100%; border-collapse: collapse; }
  .info-table td { padding: 6px 8px; font-size: 10px; width: 16%; vertical-align: top; }
  .info-lbl { color: #888; font-size: 8px; text-transform: uppercase; display: block; }
  .info-val { font-weight: bold; color: #222; }
  .section-heading { font-size: 10px; font-weight: bold; color: #1a3c6e; text-transform: uppercase; border-bottom: 1px solid #dde3ed; padding-bottom: 4px; margin-bottom: 8px; }
  .attend-table { width: 100%; border-collapse: collapse; margin-bottom: 12px; }
  .attend-table td { border: 1px solid #dde3ed; padding: 8px; text-align: center; width: 25%; }
  .attend-num { font-size: 16px; font-weight: bold; color: #1a3c6e; }
  .attend-lbl { font-size: 8px; color: #888; margin-top: 2px; }
  .salary-table { width: 100%; border-collapse: collapse; margin-bottom: 12px; }
  .salary-table th { background: #1a3c6e; color: #fff; padding: 7px 10px; text-align: left; font-size: 10px; }
  .salary-table td { padding: 6px 10px; border-bottom: 1px solid #eee; font-size: 10px; }
  .salary-table tr:nth-child(even) td { background: #f9fafb; }
  .amt { text-align: right; }
  .ded { color: #c0392b; text-align: right; }
  .total-row td { background: #edf2f7 !important; font-weight: bold; border-top: 2px solid #1a3c6e; }
  .words-box { background: #f5f7fa; border: 1px solid #dde3ed; padding: 10px 14px; margin-bottom: 12px; }
  .words-lbl { font-size: 8px; color: #888; text-transform: uppercase; margin-bottom: 4px; }
  .words-val { font-size: 11px; font-weight: bold; color: #1a3c6e; }
  .sig-table { width: 100%; border-collapse: collapse; margin-top: 20px; border-top: 1px solid #dde3ed; padding-top: 12px; }
  .sig-table td { width: 33%; padding: 8px; text-align: center; vertical-align: bottom; }
  .sig-line { border-bottom: 1px solid #333; margin-bottom: 4px; height: 25px; }
  .sig-lbl { font-size: 8px; color: #888; text-transform: uppercase; }
  .note { text-align: center; font-size: 8px; color: #aaa; margin-top: 12px; border-top: 1px solid #eee; padding-top: 8px; }
</style>
</head>
<body>
<div class="page">

  <div class="company-header">
    <div class="slip-header-right">
      <div class="slip-title-text">SALARY SLIP</div>
      <div class="slip-period">PAYPERIOD</div>
      <div class="confidential">CONFIDENTIAL</div>
    </div>
    <img src="file:///home/frappe/frappe-bench/sites/frontend/public/files/LOGO.png" style="height:50px;width:auto;margin-bottom:6px;display:block;"><div class="company-name">Atrina Technologies Pvt Ltd</div>
    <div class="company-address">C Wing, KAILASH BUSINESS PARK, P2, Park Site Rd, HMPL Surya Nagar, Vikhroli West, Mumbai 400079<br>CIN: U72900MH2020PTC123456 | PAN: AABCA1234Z</div>
    <div class="clearfix"></div>
  </div>

  <div class="info-box">
    <table class="info-table">
      <tr>
        <td><span class="info-lbl">Employee Name</span><span class="info-val">EMPNAME</span></td>
        <td><span class="info-lbl">Department</span><span class="info-val">DEPT</span></td>
        <td><span class="info-lbl">Pay Period</span><span class="info-val">PAYPERIOD</span></td>
        <td><span class="info-lbl">Date of Generation</span><span class="info-val">TODAY</span></td>
        <td><span class="info-lbl">Payment Status</span><span class="info-val" style="color:#1a7a4a;">Paid</span></td>
        <td><span class="info-lbl">Per Day Salary</span><span class="info-val">Rs PERDAYAMT</span></td>
      </tr>
    </table>
  </div>

  <div class="section-heading">Attendance Summary</div>
  <table class="attend-table">
    <tr>
      <td><div class="attend-num">26</div><div class="attend-lbl">Working Days</div></td>
      <td><div class="attend-num">PRESENTDAYS</div><div class="attend-lbl">Days Present</div></td>
      <td><div class="attend-num">ABSENTDAYS</div><div class="attend-lbl">Days Absent</div></td>
      <td><div class="attend-num">LWPDAYS</div><div class="attend-lbl">LWP Days</div></td>
    </tr>
  </table>

  <div class="section-heading">Earnings and Deductions</div>
  <table class="salary-table">
    <thead>
      <tr>
        <th style="width:40%;">Component</th>
        <th style="width:20%;">Type</th>
        <th style="width:20%; text-align:right;">Amount (Rs)</th>
        <th style="width:20%; text-align:right;">YTD (Rs)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Basic Salary</td><td>Earning</td>
        <td class="amt">BASICAMT</td><td class="amt">BASICAMT</td>
      </tr>
      <tr>
        <td>House Rent Allowance (40%)</td><td>Earning</td>
        <td class="amt">HRAAMT</td><td class="amt">HRAAMT</td>
      </tr>
      <tr>
        <td>Provident Fund (PF) - 12%</td><td>Deduction</td>
        <td class="ded">- PFAMT</td><td class="ded">- PFAMT</td>
      </tr>
      <tr>
        <td>Loss of Pay (LOP) Deduction</td><td>Deduction</td>
        <td class="ded">- LOPAMT</td><td class="ded">- LOPAMT</td>
      </tr>
      <tr class="total-row">
        <td colspan="2">Net Payable</td>
        <td class="amt">NETAMT</td><td class="amt">NETAMT</td>
      </tr>
    </tbody>
  </table>

  <div class="words-box">
    <div class="words-lbl">Net Salary Payable in Words</div>
    <div class="words-val">NETWORDS Only</div>
  </div>

  <table class="sig-table">
    <tr>
      <td><div class="sig-line"></div><div class="sig-lbl">Employee Signature</div></td>
      <td><div class="sig-line"></div><div class="sig-lbl">HR Manager</div></td>
      <td><div class="sig-line"></div><div class="sig-lbl">Authorized Signatory</div></td>
    </tr>
  </table>

  <div class="note">This is a system-generated salary slip and does not require a physical signature. | Atrina Technologies Pvt Ltd | Confidential</div>

</div>
</body>
</html>"""

            html = html.replace("EMPNAME", emp.employee_name)
            html = html.replace("DEPT", emp.department or "")
            html = html.replace("PAYPERIOD", doc.month + " " + str(doc.year))
            html = html.replace("TODAY", frappe.utils.nowdate())
            html = html.replace("PERDAYAMT", "{:,.2f}".format(per_day))
            html = html.replace("PRESENTDAYS", str(int(emp.present_days)))
            html = html.replace("ABSENTDAYS", str(int(emp.absent_days)))
            html = html.replace("LWPDAYS", str(int(emp.lwp_days)))
            html = html.replace("BASICAMT", "{:,.2f}".format(emp.basic))
            html = html.replace("HRAAMT", "{:,.2f}".format(emp.hra))
            html = html.replace("PFAMT", "{:,.2f}".format(emp.pf_deduction))
            html = html.replace("LOPAMT", "{:,.2f}".format(emp.lwp_deduction))
            html = html.replace("NETAMT", "{:,.2f}".format(emp.net_payable))
            html = html.replace("NETWORDS", "Rupees " + str(int(emp.net_payable)))

            pdf = frappe.utils.pdf.get_pdf(html, options={"enable-local-file-access": ""})
            frappe.sendmail(
                recipients=[emp_email],
                subject="Salary Slip - " + doc.month + " " + str(doc.year) + " | Atrina Technologies",
                message="Dear " + emp.employee_name + ",<br><br>Please find attached your salary slip for <b>" + doc.month + " " + str(doc.year) + "</b>.<br><br>Regards,<br>HR Team - Atrina Technologies",
                attachments=[{
                    "fname": "Salary_Slip_" + emp.employee_name + "_" + doc.month + "_" + str(doc.year) + ".pdf",
                    "fcontent": pdf
                }]
            )
            sent += 1
    frappe.db.commit()
    return "Salary slips sent to " + str(sent) + " employees"

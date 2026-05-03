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
  body { font-family: Arial, sans-serif; font-size: 12px; color: #333; background: #fff; }
  .page { width: 750px; margin: 0 auto; padding: 30px; }
  .company-header { border-bottom: 3px solid #1a3c6e; padding-bottom: 16px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: flex-end; }
  .company-name { font-size: 20px; font-weight: bold; color: #1a3c6e; }
  .company-address { font-size: 10px; color: #666; margin-top: 4px; line-height: 1.5; }
  .slip-title { text-align: right; }
  .slip-title h2 { font-size: 15px; color: #1a3c6e; font-weight: bold; }
  .slip-title p { font-size: 11px; color: #666; margin-top: 3px; }
  .confidential { display: inline-block; border: 1px solid #1a3c6e; color: #1a3c6e; font-size: 9px; padding: 2px 8px; border-radius: 3px; margin-top: 4px; letter-spacing: 1px; }
  .info-section { background: #f5f7fa; border: 1px solid #dde3ed; border-radius: 4px; padding: 12px 16px; margin-bottom: 16px; }
  .info-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }
  .info-item { display: flex; flex-direction: column; }
  .info-label { font-size: 9px; color: #888; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 2px; }
  .info-value { font-size: 12px; font-weight: bold; color: #222; }
  .attend-section { margin-bottom: 16px; }
  .section-heading { font-size: 11px; font-weight: bold; color: #1a3c6e; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #dde3ed; padding-bottom: 5px; margin-bottom: 10px; }
  .attend-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
  .attend-card { border: 1px solid #dde3ed; border-radius: 4px; padding: 8px 12px; text-align: center; }
  .attend-num { font-size: 18px; font-weight: bold; color: #1a3c6e; }
  .attend-lbl { font-size: 9px; color: #888; margin-top: 2px; }
  .salary-table { width: 100%; border-collapse: collapse; margin-bottom: 16px; }
  .salary-table th { background: #1a3c6e; color: #fff; padding: 8px 12px; text-align: left; font-size: 11px; }
  .salary-table td { padding: 7px 12px; border-bottom: 1px solid #eee; font-size: 11px; }
  .salary-table tr:nth-child(even) td { background: #f9fafb; }
  .salary-table .amount { text-align: right; }
  .salary-table .deduction { color: #c0392b; }
  .total-row td { background: #edf2f7 !important; font-weight: bold; border-top: 2px solid #1a3c6e; }
  .net-row td { background: #1a3c6e !important; color: #fff !important; font-weight: bold; font-size: 13px; }
  .footer-section { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-top: 24px; padding-top: 16px; border-top: 1px solid #dde3ed; }
  .sig-block { display: flex; flex-direction: column; }
  .sig-line { border-bottom: 1px solid #333; margin-bottom: 5px; height: 30px; }
  .sig-label { font-size: 9px; color: #888; text-transform: uppercase; letter-spacing: 0.5px; }
  .note { text-align: center; font-size: 9px; color: #aaa; margin-top: 16px; font-style: italic; border-top: 1px solid #eee; padding-top: 10px; }
</style>
</head>
<body>
<div class="page">

  <div class="company-header">
    <div>
      <div class="company-name">Atrina Technologies Pvt Ltd</div>
      <div class="company-address">C Wing, KAILASH BUSINESS PARK, P2, Park Site Rd,<br>HMPL Surya Nagar, Vikhroli West, Mumbai, Maharashtra 400079<br>CIN: U72900MH2020PTC123456 | PAN: AABCA1234Z</div>
    </div>
    <div class="slip-title">
      <h2>SALARY SLIP</h2>
      <p>Salary Slip</p>
      <span class="confidential">CONFIDENTIAL</span>
    </div>
  </div>

  <div class="info-section">
    <div class="info-grid">
      <div class="info-item">
        <span class="info-label">Employee Name</span>
        <span class="info-value">EMPNAME</span>
      </div>
      <div class="info-item">
        <span class="info-label">Department</span>
        <span class="info-value">DEPT</span>
      </div>
      <div class="info-item">
        <span class="info-label">Pay Period</span>
        <span class="info-value">MONTH YEAR</span>
      </div>
      <div class="info-item">
        <span class="info-label">Date of Generation</span>
        <span class="info-value">TODAY</span>
      </div>
      <div class="info-item">
        <span class="info-label">Payment Status</span>
        <span class="info-value" style="color:#1a7a4a;">Paid</span>
      </div>
      <div class="info-item">
        <span class="info-label">Per Day Salary</span>
        <span class="info-value">Rs PERDAY</span>
      </div>
    </div>
  </div>

  <div class="attend-section">
    <div class="section-heading">Attendance Summary</div>
    <div class="attend-grid">
      <div class="attend-card">
        <div class="attend-num">26</div>
        <div class="attend-lbl">Working Days</div>
      </div>
      <div class="attend-card">
        <div class="attend-num">PRESENT</div>
        <div class="attend-lbl">Days Present</div>
      </div>
      <div class="attend-card">
        <div class="attend-num">ABSENT</div>
        <div class="attend-lbl">Days Absent</div>
      </div>
      <div class="attend-card">
        <div class="attend-num">LWP</div>
        <div class="attend-lbl">LWP Days</div>
      </div>
    </div>
  </div>

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
        <td>Basic Salary</td>
        <td>Earning</td>
        <td class="amount">BASIC</td>
        <td class="amount">BASIC</td>
      </tr>
      <tr>
        <td>House Rent Allowance (40%)</td>
        <td>Earning</td>
        <td class="amount">HRAAMT</td>
        <td class="amount">HRAAMT</td>
      </tr>
      <tr>
        <td>Provident Fund (PF) - 12%</td>
        <td>Deduction</td>
        <td class="amount deduction">- PFDED</td>
        <td class="amount deduction">- PFDED</td>
      </tr>
      <tr>
        <td>Loss of Pay (LOP) Deduction</td>
        <td>Deduction</td>
        <td class="amount deduction">- LWPDED</td>
        <td class="amount deduction">- LWPDED</td>
      </tr>
      <tr class="total-row">
        <td colspan="2">Net Payable</td>
        <td class="amount">NETPAY</td>
        <td class="amount">NETPAY</td>
      </tr>
    </tbody>
  </table>

  <div style="background:#f5f7fa; border:1px solid #dde3ed; border-radius:4px; padding:12px 16px; margin-bottom:16px;">
    <div style="font-size:9px; color:#888; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px;">Net Salary Payable in Words</div>
    <div style="font-size:12px; font-weight:bold; color:#1a3c6e;">NETWORDS Only</div>
  </div>

  <div class="footer-section">
    <div class="sig-block">
      <div class="sig-line"></div>
      <div class="sig-label">Employee Signature</div>
    </div>
    <div class="sig-block">
      <div class="sig-line"></div>
      <div class="sig-label">HR Manager</div>
    </div>
    <div class="sig-block">
      <div class="sig-line"></div>
      <div class="sig-label">Authorized Signatory</div>
    </div>
  </div>

  <div class="note">
    This is a system-generated salary slip and does not require a physical signature. | Atrina Technologies Pvt Ltd | Confidential
  </div>

</div>
</body>
</html>"""

            html = html.replace("EMPNAME", emp.employee_name)
            html = html.replace("MONTH", doc.month)
            html = html.replace("YEAR", str(doc.year))
            html = html.replace("DEPT", emp.department or "")
            html = html.replace("TODAY", frappe.utils.nowdate())
            html = html.replace("PERDAY", "{:,.2f}".format(per_day))
            html = html.replace("PRESENT", str(int(emp.present_days)))
            html = html.replace("ABSENT", str(int(emp.absent_days)))
            html = html.replace("LWP", str(int(emp.lwp_days)))
            html = html.replace("BASIC", "{:,.2f}".format(emp.basic))
            html = html.replace("HRAAMT", "{:,.2f}".format(emp.hra))
            html = html.replace("PFDED", "{:,.2f}".format(emp.pf_deduction))
            html = html.replace("LWPDED", "{:,.2f}".format(emp.lwp_deduction))
            html = html.replace("NETPAY", "{:,.2f}".format(emp.net_payable))
            html = html.replace("Salary Slip", "Payslip for " + doc.month + " " + str(doc.year))
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

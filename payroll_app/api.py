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
            html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body { font-family: Arial, sans-serif; font-size: 13px; color: #222; margin: 0; padding: 0; }
  .slip { max-width: 780px; margin: 0 auto; padding: 32px; border: 1px solid #ddd; }
  .header { display: flex; align-items: center; gap: 18px; background: #1a3c6e; padding: 20px 24px; border-radius: 6px; margin-bottom: 20px; }
  .header img { height: 56px; width: auto; }
  .header-text .company { font-size: 20px; font-weight: bold; color: #fff; }
  .header-text .address { font-size: 11px; color: #b0c4de; margin-top: 3px; }
  .header-text .payslip-for { font-size: 13px; color: #fff; margin-top: 6px; }
  .badge { display: inline-block; background: #fff; color: #1a3c6e; font-size: 11px; font-weight: bold; padding: 3px 10px; border-radius: 12px; margin-top: 6px; }
  .divider { border: none; border-top: 2px solid #1a3c6e; margin: 16px 0; }
  .info-table { width: 100%; border-collapse: collapse; margin: 10px 0; }
  .info-table td { padding: 6px 10px; font-size: 13px; }
  .info-table .label { color: #555; width: 22%; }
  .info-table .colon { width: 2%; color: #555; }
  .info-table .value { font-weight: 600; color: #111; width: 26%; }
  .section-title { background: #1a3c6e; color: #fff; padding: 8px 14px; font-size: 13px; font-weight: bold; border-radius: 4px 4px 0 0; margin-top: 16px; }
  .attend-box { display: flex; gap: 12px; margin: 12px 0; }
  .attend-card { flex: 1; background: #f0f5ff; border: 1px solid #b0c4de; border-radius: 6px; padding: 10px 14px; text-align: center; }
  .attend-card .num { font-size: 22px; font-weight: bold; color: #1a3c6e; }
  .attend-card .lbl { font-size: 11px; color: #555; margin-top: 2px; }
  .earn-ded { width: 100%; border-collapse: collapse; margin-top: 0; }
  .earn-ded thead tr th { background: #1a3c6e; color: #fff; padding: 10px 14px; font-size: 13px; text-align: left; width: 25%; }
  .earn-ded tbody td { padding: 9px 14px; border-bottom: 1px solid #eee; width: 25%; }
  .earn-ded tbody tr:nth-child(even) td { background: #f7faff; }
  .total-row td { background: #e8f0fe !important; border-top: 2px solid #1a3c6e; font-weight: bold; padding: 10px 14px; }
  .net-row td { background: #1a3c6e; color: #fff; padding: 12px 14px; font-size: 15px; font-weight: bold; }
  .footer-table { width: 100%; margin-top: 24px; }
  .footer-table td { width: 33%; vertical-align: bottom; padding: 4px 8px; }
  .footer-label { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 0.5px; }
  .footer-val { font-size: 13px; font-weight: bold; margin-top: 3px; color: #1a3c6e; }
  .sig-line { font-size: 15px; margin-top: 28px; color: #aaa; }
  .slip-note { text-align: center; font-size: 11px; color: #aaa; font-style: italic; margin-top: 20px; padding-top: 12px; border-top: 1px solid #eee; }
  .summary-cards { display: flex; gap: 12px; margin: 16px 0; }
  .summary-card { flex: 1; border-radius: 6px; padding: 12px 14px; text-align: center; }
  .summary-card.earning { background: #e8f5e9; border: 1px solid #a5d6a7; }
  .summary-card.deduction { background: #fff3e0; border: 1px solid #ffcc80; }
  .summary-card.net { background: #1a3c6e; border: 1px solid #1a3c6e; }
  .summary-card .amt { font-size: 18px; font-weight: bold; }
  .summary-card.earning .amt { color: #2e7d32; }
  .summary-card.deduction .amt { color: #e65100; }
  .summary-card.net .amt { color: #fff; }
  .summary-card .slbl { font-size: 11px; margin-top: 3px; }
  .summary-card.earning .slbl { color: #555; }
  .summary-card.deduction .slbl { color: #555; }
  .summary-card.net .slbl { color: #b0c4de; }
</style>
</head>
<body>
<div class="slip">
  <div class="header">
    <img src="file:///home/frappe/frappe-bench/sites/frontend/public/files/LOGO.png">
    <div class="header-text">
      <div class="company">Atrina Technologies Pvt Ltd</div>
      <div class="address">C Wing, KAILASH BUSINESS PARK, P2, Park Site Rd, HMPL Surya Nagar, Vikhroli West, Mumbai 400079</div>
      <div class="payslip-for">Pay Slip for {doc.month} {doc.year}</div>
      <div class="badge">CONFIDENTIAL</div>
    </div>
  </div>

  <div class="section-title">Employee Details</div>
  <table class="info-table">
    <tr>
      <td class="label">Employee Name</td><td class="colon">:</td>
      <td class="value"><b>{emp.employee_name}</b></td>
      <td class="label">Month</td><td class="colon">:</td>
      <td class="value"><b>{doc.month} {doc.year}</b></td>
    </tr>
    <tr>
      <td class="label">Department</td><td class="colon">:</td>
      <td class="value">{emp.department}</td>
      <td class="label">Date of Generation</td><td class="colon">:</td>
      <td class="value">{frappe.utils.nowdate()}</td>
    </tr>
    <tr>
      <td class="label">Status</td><td class="colon">:</td>
      <td class="value" style="color:#1a3c6e;"><b>Paid</b></td>
      <td class="label">Per Day Salary</td><td class="colon">:</td>
      <td class="value">₹{per_day:,.2f}</td>
    </tr>
  </table>

  <div class="section-title" style="margin-top:16px;">Attendance Summary</div>
  <div class="attend-box">
    <div class="attend-card">
      <div class="num">26</div>
      <div class="lbl">Total Working Days</div>
    </div>
    <div class="attend-card">
      <div class="num">{emp.present_days}</div>
      <div class="lbl">Present Days</div>
    </div>
    <div class="attend-card">
      <div class="num">{emp.absent_days}</div>
      <div class="lbl">Absent Days</div>
    </div>
    <div class="attend-card">
      <div class="num">{emp.lwp_days}</div>
      <div class="lbl">LWP Days</div>
    </div>
  </div>

  <div class="summary-cards">
    <div class="summary-card earning">
      <div class="amt">₹{total_earnings:,.2f}</div>
      <div class="slbl">Total Earnings</div>
    </div>
    <div class="summary-card deduction">
      <div class="amt">₹{total_deductions:,.2f}</div>
      <div class="slbl">Total Deductions</div>
    </div>
    <div class="summary-card net">
      <div class="amt">₹{emp.net_payable:,.2f}</div>
      <div class="slbl">Net Payable</div>
    </div>
  </div>

  <div class="section-title">Salary Breakdown</div>
  <table class="earn-ded">
    <thead>
      <tr>
        <th colspan="2">Earnings</th>
        <th colspan="2">Deductions</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Basic Salary</td>
        <td>₹{emp.basic:,.2f}</td>
        <td>PF Deduction (12%)</td>
        <td>₹{emp.pf_deduction:,.2f}</td>
      </tr>
      <tr>
        <td>HRA (40%)</td>
        <td>₹{emp.hra:,.2f}</td>
        <td>LWP Deduction</td>
        <td>₹{emp.lwp_deduction:,.2f}</td>
      </tr>
      <tr class="total-row">
        <td><b>Total Earnings</b></td>
        <td><b>₹{total_earnings:,.2f}</b></td>
        <td><b>Total Deductions</b></td>
        <td><b>₹{total_deductions:,.2f}</b></td>
      </tr>
    </tbody>
    <tfoot>
      <tr class="net-row">
        <td colspan="3" style="text-align:right;">Net Salary</td>
        <td>₹{emp.net_payable:,.2f}</td>
      </tr>
    </tfoot>
  </table>

  <hr class="divider">
  <table class="footer-table">
    <tr>
      <td>
        <div class="footer-label">Generated By</div>
        <div class="footer-val">HR Team - Atrina Technologies</div>
      </td>
      <td style="text-align:center;">
        <div class="footer-label">Employee Signature</div>
        <div class="sig-line">_______________________</div>
      </td>
      <td style="text-align:right;">
        <div class="footer-label">Authorized Signature</div>
        <div class="sig-line">_______________________</div>
      </td>
    </tr>
  </table>
  <div class="slip-note">This is a computer generated payslip and does not require a physical signature.</div>
</div>
</body>
</html>"""
            pdf = frappe.utils.pdf.get_pdf(html, options={"enable-local-file-access": ""})
            frappe.sendmail(
                recipients=[emp_email],
                subject=f"Salary Slip - {doc.month} {doc.year} | Atrina Technologies",
                message=f"""Dear {emp.employee_name},<br><br>
Please find attached your salary slip for <b>{doc.month} {doc.year}</b>.<br><br>
Regards,<br>
HR Team - Atrina Technologies""",
                attachments=[{
                    "fname": f"Salary_Slip_{emp.employee_name}_{doc.month}_{doc.year}.pdf",
                    "fcontent": pdf
                }]
            )
            sent += 1
    frappe.db.commit()
    return f"Salary slips sent to {sent} employees"

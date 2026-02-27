from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Assessment
from .forms import AssessmentForm
from .services import (
    calculate_total_score,
    calculate_penalty,
    calculate_risk,
    calculate_section_status,  # ✅ Added only
)
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch


@login_required
def dashboard(request):
    assessments = Assessment.objects.filter(
        tenant=request.user.tenant
    ).order_by("-created_at")

    latest_assessment = assessments.first()

    context = {
        "assessments": assessments,
        "latest_assessment": latest_assessment,
        "total_count": assessments.count(),
    }

    return render(request, "dashboard.html", context)

@login_required
def executive_summary(request):
    assessments = Assessment.objects.filter(
        tenant=request.user.tenant
    ).order_by("-created_at")

    latest = assessments.first()

    return render(request, "executive_summary.html", {
        "latest": latest
    })

@login_required
def create_assessment(request):

    if request.method == "POST":
        form = AssessmentForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            total_score = calculate_total_score(
                data["consent"],
                data["security"],
                data["breach"],
                data["children"],
                data["sdf"],
            )

            penalty = calculate_penalty(data)
            risk = calculate_risk(total_score, penalty)

            # ✅ NEW: Calculate section-wise legal status
            section_status = calculate_section_status(data)

            Assessment.objects.create(
                tenant=request.user.tenant,
                consent_score=data["consent"],
                security_score=data["security"],
                breach_score=data["breach"],
                children_score=data["children"],
                sdf_score=data["sdf"],
                total_score=total_score,
                penalty_exposure=penalty,
                risk_level=risk,

                # ✅ NEW: Save section breakdown (No original code removed)
                section_8_5_status=section_status["section_8_5"],
                section_8_6_status=section_status["section_8_6"],
                section_9_status=section_status["section_9"],
                section_10_status=section_status["section_10"],
            )

            return redirect("dashboard")
    else:
        form = AssessmentForm()

    return render(request, "assessment_form.html", {"form": form})


@login_required
def generate_pdf(request, assessment_id):
    from .models import Assessment

    assessment = Assessment.objects.get(
        id=assessment_id,
        tenant=request.user.tenant
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="DPDP_Report_{assessment.id}.pdf"'

    doc = SimpleDocTemplate(response)
    elements = []

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    normal_style = styles["Normal"]

    elements.append(Paragraph("DPDP Compliance Assessment Report", title_style))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"Company: {request.user.tenant.name}", normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"Assessment Date: {assessment.created_at.strftime('%Y-%m-%d %H:%M')}", normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"Compliance Score: {assessment.total_score}%", normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"Risk Level: {assessment.risk_level}", normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"Potential Penalty Exposure: ₹ {assessment.penalty_exposure} Crore", normal_style))
    elements.append(Spacer(1, 0.5 * inch))
    
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph("Section Compliance:", title_style))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"Section 8(5): {assessment.section_8_5_status}", normal_style))
    elements.append(Paragraph(f"Section 8(6): {assessment.section_8_6_status}", normal_style))
    elements.append(Paragraph(f"Section 9: {assessment.section_9_status}", normal_style))
    elements.append(Paragraph(f"Section 10: {assessment.section_10_status}", normal_style))

    disclaimer = """
    Disclaimer: Penalty exposure reflects statutory maximum limits under the
    Digital Personal Data Protection Act schedule. Final determination rests
    with the Data Protection Board of India.
    """

    elements.append(Paragraph(disclaimer, normal_style))

    doc.build(elements)

    return response
"""Populate the AI Solutions demonstration site with practical sample content."""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from core.models import Article, CaseStudy, PromotionalEvent, Solution, Testimonial


class Command(BaseCommand):
    help = "Seed the database with AI Solutions demonstration content"

    def handle(self, *args, **options):
        self._seed_solutions()
        self._seed_case_studies()
        self._seed_testimonials()
        self._seed_articles()
        self._seed_promotional_events()
        self.stdout.write(self.style.SUCCESS("AI Solutions demo content is ready."))

    def _seed_solutions(self):
        records = [
            {
                "title": "Staff help desk",
                "icon": "support",
                "summary": "A clear front door for IT, people and workplace requests.",
                "description": "Collect routine staff questions in one place, provide immediate guidance and pass complex work to the correct team with context attached.",
                "features": "Web and Teams access\nKnowledge library\nTeam handover\nRequest history",
                "is_featured": True,
                "display_order": 1,
            },
            {
                "title": "Request workflows",
                "icon": "workflow",
                "summary": "Structured approvals and follow-up for recurring work.",
                "description": "Replace shared inbox chasing with defined steps, ownership, reminders and a reliable record of decisions.",
                "features": "Approval routing\nAutomatic reminders\nAudit history\nProgress tracking",
                "is_featured": True,
                "display_order": 2,
            },
            {
                "title": "People services",
                "icon": "support",
                "summary": "Everyday HR requests handled through a familiar channel.",
                "description": "Support leave requests, policy access, onboarding tasks and payroll questions without adding administration for the people team.",
                "features": "Leave and absence\nStarter tasks\nPolicy library\nPayroll requests",
                "is_featured": True,
                "display_order": 3,
            },
            {
                "title": "Service reporting",
                "icon": "chart",
                "summary": "Useful reporting on demand, completion and recurring issues.",
                "description": "Give service managers a concise view of volumes, turnaround times and where teams need practical improvement.",
                "features": "Daily reporting\nTrend review\nExports\nAccess controls",
                "is_featured": False,
                "display_order": 4,
            },
            {
                "title": "System connections",
                "icon": "integration",
                "summary": "Connect existing business tools without replacing them.",
                "description": "Pass requests and status updates between your established platforms using supported connections and documented endpoints.",
                "features": "Microsoft 365\nServiceNow\nWorkday\nREST endpoints",
                "is_featured": False,
                "display_order": 5,
            },
            {
                "title": "Security controls",
                "icon": "shield",
                "summary": "Access, audit records and appropriate information handling.",
                "description": "Apply controlled access and maintain records suitable for workplace service processes and internal review.",
                "features": "Role access\nAudit records\nData residency options\nReview reporting",
                "is_featured": False,
                "display_order": 6,
            },
        ]
        old_titles = [
            "Intelligent Virtual Assistant",
            "Workflow Automation Engine",
            "HR Self-Service Portal",
            "Analytics & Insights Dashboard",
            "Enterprise Integration Hub",
            "Security & Compliance Suite",
        ]
        for old_title, data in zip(old_titles, records):
            obj = Solution.objects.filter(title=old_title).first()
            if obj:
                for field, value in data.items():
                    setattr(obj, field, value)
                obj.save()
            else:
                Solution.objects.update_or_create(title=data["title"], defaults=data)

    def _seed_case_studies(self):
        records = [
            ("NorthernCare NHS Trust", {"client_name": "Northshore Health Trust", "industry": "Healthcare", "challenge": "Repeated access and password requests were holding up a small IT support team.", "solution": "Introduced a staff help desk connected to the existing service management process.", "outcome": "Routine requests were resolved in minutes and the team regained capacity for complex work.", "metric_label": "fewer IT helpdesk calls", "metric_value": "38%"}),
            ("TechRetail UK", {"client_name": "Field & Found", "industry": "Retail", "challenge": "Store teams needed quicker access to rota and payroll information.", "solution": "Connected a people-services request channel with the existing HR platform.", "outcome": "Requests moved away from shared inboxes and HR administration reduced.", "metric_label": "staff adoption in two weeks", "metric_value": "94%"}),
            ("FinServe Group", {"client_name": "Tyne Ledger", "industry": "Financial Services", "challenge": "New starter approvals passed manually through four departments.", "solution": "Set up sequenced onboarding tasks with reminders and an audit history.", "outcome": "Onboarding moved from three weeks to four working days.", "metric_label": "saved each week", "metric_value": "22 hrs"}),
            ("LogiPlus Distribution", {"client_name": "Portline Distribution", "industry": "Distribution", "challenge": "Depot teams spent too much time responding to routine shipment queries.", "solution": "Connected shipment tracking to a driver and customer request channel.", "outcome": "Support staff focused on exceptions while routine status checks were handled immediately.", "metric_label": "routine queries handled", "metric_value": "91%"}),
        ]
        for old_name, data in records:
            obj = CaseStudy.objects.filter(client_name=old_name).first()
            if obj:
                for field, value in data.items():
                    setattr(obj, field, value)
                obj.save()
            else:
                CaseStudy.objects.update_or_create(client_name=data["client_name"], defaults=data)

    def _seed_testimonials(self):
        records = [
            ("Sarah Mitchell", {"author_name": "Helen Ward", "author_title": "Service Manager, Northshore Health Trust", "quote": "Our IT team now spends far less time on access queries. Staff know exactly where their request stands.", "rating": 5}),
            ("James Okafor", {"author_name": "Malcolm Reed", "author_title": "Operations Director, Field & Found", "quote": "The rollout was calm and practical. Store colleagues adopted the request process in the first fortnight.", "rating": 5}),
            ("Priya Sharma", {"author_name": "Anita Rowe", "author_title": "People Lead, Tyne Ledger", "quote": "Approval history is now visible in one place, which has made onboarding considerably easier to manage.", "rating": 5}),
        ]
        for old_name, data in records:
            obj = Testimonial.objects.filter(author_name=old_name).first()
            if obj:
                for field, value in data.items():
                    setattr(obj, field, value)
                obj.save()
            else:
                Testimonial.objects.update_or_create(author_name=data["author_name"], defaults=data)

    def _seed_articles(self):
        records = [
            ("roi-of-ai-modern-workplace", {"title": "Finding the hidden cost of routine requests", "slug": "cost-of-routine-requests", "category": "insight", "excerpt": "A straightforward way to measure repeated service work before changing a process.", "body": "<p>Small requests can consume a surprising amount of a team's time when they arrive in different inboxes and cannot be tracked consistently.</p><h3>Measure before changing</h3><p>Record request types, ownership and completion time for a short period. That evidence makes it easier to choose a sensible first improvement.</p>", "author": "AI Solutions Delivery Team", "read_time_min": 6, "is_published": True}),
            ("deploying-first-ai-chatbot-guide", {"title": "Starting with one service workflow", "slug": "starting-with-one-service-workflow", "category": "tutorial", "excerpt": "How to choose a useful first process, map ownership and run a manageable pilot.", "body": "<p>A useful service project begins with one repeatable process and a clear owner.</p><h3>Choose manageable work</h3><p>Look for frequent requests with clear outcomes, then agree how success will be measured before making changes.</p>", "author": "AI Solutions Delivery Team", "read_time_min": 8, "is_published": True}),
            ("soc2-type-ii-certification", {"title": "AI Solutions publishes its service security controls", "slug": "ai-solutions-service-security-controls", "category": "news", "excerpt": "An update on access management, audit history and information handling.", "body": "<p>Clients need to understand how service information is accessed and recorded. AI Solutions has published a clear overview of its operating controls for prospective customers.</p><h3>Request a copy</h3><p>Contact our team to discuss controls relevant to your process and organisation.</p>", "author": "AI Solutions Team", "read_time_min": 3, "is_published": True}),
        ]
        for old_slug, data in records:
            previous_brand_slug = data["slug"].replace("ai-solutions", "wearbridge")
            obj = Article.objects.filter(
                slug__in=[old_slug, previous_brand_slug, data["slug"]]
            ).first()
            if obj:
                for field, value in data.items():
                    setattr(obj, field, value)
                obj.save()
            else:
                Article.objects.update_or_create(slug=data["slug"], defaults=data)

    def _seed_promotional_events(self):
        today = timezone.localdate()
        records = [
            {
                "title": "Making service requests easier to track",
                "event_type": "workshop",
                "event_date": today + timedelta(days=21),
                "location": "Sunderland Software City",
                "description": "A practical working session for operations teams planning a first service workflow improvement.",
                "registration_label": "Register interest",
                "is_published": True,
            },
            {
                "title": "Reducing HR administration for growing teams",
                "event_type": "networking",
                "event_date": today + timedelta(days=45),
                "location": "Manchester",
                "description": "A small roundtable on request routing, onboarding visibility and people-service reporting.",
                "registration_label": "Contact us",
                "is_published": True,
            },
            {
                "title": "Inside a workplace service rollout",
                "event_type": "conference",
                "event_date": today + timedelta(days=70),
                "location": "Sunderland",
                "description": "An open studio session showing how AI Solutions moves from query to pilot delivery.",
                "registration_label": "Register interest",
                "is_published": True,
            },
        ]
        for data in records:
            PromotionalEvent.objects.update_or_create(
                title=data["title"],
                defaults=data,
            )

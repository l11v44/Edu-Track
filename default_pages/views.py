from django.shortcuts import render

from django.views.generic import TemplateView

class AboutView(TemplateView): template_name = 'default_pages/about.html'
class ManifestoView(TemplateView): template_name = 'default_pages/manifesto.html'
class MethodologyView(TemplateView): template_name = 'default_pages/methodology.html'
class SecurityView(TemplateView): template_name = 'default_pages/security.html'
class CareersView(TemplateView): template_name = 'default_pages/careers.html'
class InvestorsView(TemplateView): template_name = 'default_pages/investors.html'
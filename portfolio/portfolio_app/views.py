from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import redirect
from .models import Student, Portfolio, Project
from .forms import ProjectForm, PortfolioForm


def index(request):
   student_active_portfolios = Student.objects.select_related('portfolio').all().filter(portfolio__is_active=True)

   print("active portfolio query set", student_active_portfolios)
   
   return render( request, 'portfolio_app/index.html', {'student_active_portfolios':student_active_portfolios})


def createProject(request, portfolio_id): # Gets portfolio_id from the URL, <int:portfolio_id>
    form = ProjectForm()
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    
    if request.method == 'POST':
        # Create a new dictionary with form data and portfolio_id
        project_data = request.POST.copy()
        project_data['portfolio_id'] = portfolio_id
        
        form = ProjectForm(project_data)
        if form.is_valid():
            # Save the form without committing to the database
            project = form.save(commit=False)
            # Set the portfolio relationship
            project.portfolio = portfolio
            project.save()

            # Redirect back to the portfolio detail page
            return redirect('portfolio-detail', portfolio_id)

    context = {'form': form}
    return render(request, 'portfolio_app/project_form.html', context)


def updateProject(request, portfolio_id, project_id): # Gets portfolio_id and project_id from the URL, <int:portfolio_id>/<int:project_id>
      project = Project.objects.get(pk=project_id)

      if request.method == 'POST':
         # Gets form data from the POST request
         new_project_data = request.POST.copy()
         # New form must be created to validate the data
         form = ProjectForm(new_project_data)
         if form.is_valid():
            project.title = form.data['title']
            project.description = form.data['description']
            project.save() # Save the updated project to the database

            return redirect('portfolio-detail', portfolio_id)

      # ----GET request from update button in portfolio_detail.html----
      # data must be a dictionary to be passed to the form, with
      # the keys being the field names in forms.py
      data = {'title': project.title, 'description': project.description}
      form = ProjectForm(data)
      context = {'form': form} # context is needed to pass the form with data to the template
      return render(request, 'portfolio_app/project_form.html', context)

def updatePortfolio(request, portfolio_id):
   portfolio = Portfolio.objects.get(pk=portfolio_id)

   if request.method == 'POST':
      # Gets form data from the POST request
      new_portfolio_data = request.POST.copy()

      # New form must be created to validate the data
      form = PortfolioForm(new_portfolio_data)
      if form.is_valid():
         # Update the portfolio object with the new data an save to the database
         portfolio.title = form.data['title']
         # form.cleaned_data returns a dictionary of validated form input fields and their values
         # without it you get a MultiValueDictKeyError
         portfolio.is_active = form.cleaned_data['is_active']

         portfolio.about = form.data['about']
         portfolio.contact_email = form.data['contact_email']
         portfolio.save()

         return redirect('portfolio-detail', portfolio_id)

   # ----GET request from update button in portfolio_detail ----
   # data must be a dictionary to be passed to the form, with
   # the keys being the field names in forms.py
   data = {'title': portfolio.title, 'is_active': portfolio.is_active, 'about': portfolio.about, 'contact_email': portfolio.contact_email}
   form = PortfolioForm(data)
   context = {'form': form} # context is needed to pass the form with data to the template
   return render(request, 'portfolio_app/portfolio_update.html', context)


def deleteProject(request, project_id):
   project_to_delete = Project.objects.get(pk=project_id)

   # Get the portfolio_id for the return URL
   portfolio_id = project_to_delete.portfolio.pk

   # POST request sent by form in project_confirm_delete.html
   if request.method == 'POST':
      project_to_delete.delete()
      # return to portfolio detail view
      return redirect('portfolio-detail', portfolio_id)
   return render(request, 'portfolio_app/index.html', portfolio_id)
   

class DeleteProjectConfirmView(generic.DetailView):
   model = Project
   template_name = 'portfolio_app/project_confirm_delete.html'

class StudentListView(generic.ListView):
   model = Student

class StudentDetailView(generic.DetailView):
   model = Student

class PortfolioDetailView(generic.DetailView):
   model = Portfolio

   def get_context_data(self, **kwargs):
      context = super(PortfolioDetailView, self).get_context_data(**kwargs)
      context['projects_in_portfolio'] = Project.objects.filter(portfolio=self.object)
      return context

class ProjectListView(generic.ListView):
   model = Project

class ProjectDetailView(generic.DetailView):
   model = Project

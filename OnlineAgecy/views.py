#!python
#OnlineAgesy/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *

@login_required(login_url="login/")
def home(request):
	return render(request, "static_pages/home.html")



#--------------------Clients Views------------------------------#
#################################################################


@login_required(login_url="login/")
def clients(request):
	# get the blog clients that are published
	clients = Client.objects.raw('SELECT * FROM OnlineAgecy_client')

	# now return the rendered template
	return render(request, "clients/clients_list.html", {'clients': clients})

@login_required(login_url="login/")
def client_new(request):

    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            return redirect('clients')
    else:
        form = ClientForm()
    return render(request, 'layouts/form.html', {'form': form})


@login_required(login_url="login/")
def client_detail(request, id):
    client = get_object_or_404(Client, id=id)
    return render(request, 'clients/client_detail.html', {'client': client})


@login_required(login_url="login/")
def client_edit(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            return redirect('client_detail', id=id)
    else:
        form = ClientForm(instance=client)
    return render(request, 'layouts/form.html', {'form': form})

@login_required(login_url="login/")
def delete_client(request, id):
    query = Client.objects.get(id=id)
    query.delete()
    return redirect('clients')

@login_required(login_url="login/")
def all_clients_contracts(request, id):
	# get the blog clients that are published
	items = Contract.objects.raw('SELECT * FROM OnlineAgecy_contract WHERE Client_id_id =' + id)
	# now return the rendered template
	return render(request, "clients/allUserContracts.html", {'items': items})

@login_required(login_url="login/")
def all_clients_briefs(request, id):
	# get the blog clients that are published
	items = Brief.objects.raw('SELECT * FROM OnlineAgecy_brief WHERE Client_id_id =' + id)
	# now return the rendered template
	return render(request, "clients/allUserBriefs.html", {'items': items})

@login_required(login_url="login/")
def clients_services_count(request):
    items = Client.objects.raw('SELECT OnlineAgecy_client.Name, count(OnlineAgecy_contract_Services.id) AS num, OnlineAgecy_client.id, OnlineAgecy_contract.id '
                               'FROM (OnlineAgecy_client INNER JOIN OnlineAgecy_contract ON OnlineAgecy_client.id = OnlineAgecy_contract.Client_id_id)INNER JOIN OnlineAgecy_contract_Services ON OnlineAgecy_contract_Services.contract_id = OnlineAgecy_contract.id '
                               'GROUP BY OnlineAgecy_client.id '
                               'ORDER BY  count(OnlineAgecy_contract_Services.id) DESC')
    return render(request, 'clients/clients_services.html', {'items': items})

def all_clients_bills(request, id):
    items = Client.objects.raw('SELECT OnlineAgecy_client.id, OnlineAgecy_client.Name AS Name, OnlineAgecy_contract.id, OnlineAgecy_act.id, OnlineAgecy_bill.Act_id_id AS Act_id '
                               'FROM ((OnlineAgecy_client INNER JOIN OnlineAgecy_contract ON OnlineAgecy_client.id = OnlineAgecy_contract.Client_id_id) INNER JOIN OnlineAgecy_act ON OnlineAgecy_contract.id = OnlineAgecy_act.Contract_id_id) INNER JOIN OnlineAgecy_bill ON OnlineAgecy_act.id=OnlineAgecy_bill.Act_id_id '
                               'WHERE OnlineAgecy_client.id =' + id)
    return render(request, 'clients/allUserBiils.html', {'items': items})

def fresh_clients(request):
    items = Client.objects.raw('SELECT id ,Name FROM OnlineAgecy_client WHERE id NOT IN (SELECT Client_id_id '
                               'FROM OnlineAgecy_contract WHERE NOT EXISTS (SELECT service_id  '
                               'FROM OnlineAgecy_contract_Services WHERE service_id = OnlineAgecy_contract.id))')
    return render(request, 'clients/blacklist.html', {'items': items})

#--------------------Contracts Views------------------------------#
###################################################################


@login_required(login_url="login/")
def contracts(request):
	# get the blog clients that are published
	contracts = Contract.objects.raw('SELECT * FROM OnlineAgecy_contract')
	# now return the rendered template
	return render(request, "contracts/contracts_list.html", {'contracts': contracts})


@login_required(login_url="login/")
def contract_new(request):
    if request.method == "POST":
        form = ContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.save()
            form.save_m2m()
            return redirect('contracts')
    else:
        form = ContractForm()
    return render(request, 'layouts/form.html', {'form': form})


@login_required(login_url="login/")
def contract_detail(request, id):
    contract = get_object_or_404(Contract, id=id)
    return render(request, 'contracts/contract_detail.html', {'contract': contract})

@login_required(login_url="login/")
def contract_edit(request, id):
    contract = get_object_or_404(Contract, id=id)
    if request.method == "POST":
        form = ContractForm(request.POST, instance=contract)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.save()
            return redirect('contract_detail', id=id)
    else:
        form = ContractForm(instance=contract)
    return render(request, 'layouts/form.html', {'form': form})


@login_required(login_url="login/")
def contracts_by_date(request, Date):
    contracts = Contract.objects.raw('SELECT * FROM OnlineAgecy_contract WHERE Date =' + Date)
    return render(request, "contracts/contracts_list.html", {'contracts': contracts})

@login_required(login_url="login/")
def delete_contract(request, id):
    query = Contract.objects.get(id=id)
    query.delete()
    return redirect('contracts')

@login_required(login_url="login/")
def contracts_services(request):
    items = Contract.objects.raw('SELECT OnlineAgecy_client.id, OnlineAgecy_client.Name AS clientName , OnlineAgecy_contract.id, OnlineAgecy_contract.Client_id_id,  OnlineAgecy_contract_Services.contract_id, OnlineAgecy_service.id, OnlineAgecy_service.Name AS service, OnlineAgecy_contract_Services.service_id AS id '
                                     'FROM ((OnlineAgecy_service INNER JOIN OnlineAgecy_contract_Services ON OnlineAgecy_contract_Services.service_id = OnlineAgecy_service.id) INNER JOIN OnlineAgecy_contract ON OnlineAgecy_contract_Services.contract_id = OnlineAgecy_contract.id) INNER  JOIN OnlineAgecy_client ON OnlineAgecy_client.id = OnlineAgecy_contract.Client_id_id')
    return render(request, "contracts/contracts_services.html", {'items': items})


#--------------------Manager Views------------------------------#
#################################################################



@login_required(login_url="login/")
def managers(request):
	# get the blog clients that are published
	managers = Manager.objects.raw('SELECT * FROM OnlineAgecy_manager')
	# now return the rendered template
	return render(request, "manager/manager_list.html", {'managers': managers})


@login_required(login_url="login/")
def manager_new(request):
    if request.method == "POST":
        form = ManagerForm(request.POST)
        if form.is_valid():
            manager = form.save(commit=False)
            manager.save()
            return redirect('managers')
    else:
        form = ManagerForm()
    return render(request, 'layouts/form.html', {'form': form})


@login_required(login_url="login/")
def manager_detail(request, id):
    manager = get_object_or_404(Manager, id=id)
    return render(request, 'manager/manager_detail.html', {'manager': manager})

@login_required(login_url="login/")
def manager_edit(request, id):
    manager = get_object_or_404(Manager, id=id)
    if request.method == "POST":
        form = ManagerForm(request.POST, instance=manager)
        if form.is_valid():
            manager = form.save(commit=False)
            manager.save()
            return redirect('manager_detail', id=id)
    else:
        form = ManagerForm(instance=manager)
    return render(request, 'layouts/form.html', {'form': form})

@login_required(login_url="login/")
def managers_clients_count(request):
    items = Manager.objects.raw('SELECT OnlineAgecy_manager.Name, count(OnlineAgecy_client.id) AS num, OnlineAgecy_contract.id FROM (OnlineAgecy_manager INNER JOIN OnlineAgecy_contract ON OnlineAgecy_manager.id = OnlineAgecy_contract.Manager_id_id)INNER JOIN OnlineAgecy_client ON OnlineAgecy_contract.Manager_id_id = OnlineAgecy_client.id GROUP BY OnlineAgecy_client.id ORDER BY  count(OnlineAgecy_client.id) DESC')
    return render(request, 'manager/manager_clients.html', {'items': items})

@login_required(login_url="login/")
def delete_manager(request, id):
    query = Manager.objects.get(id=id)
    query.delete()
    return redirect('managers')
#--------------------Brief Views------------------------------#
###############################################################

@login_required(login_url="login/")
def brief(request):
	# get the blog clients that are published
	briefs = Brief.objects.raw('SELECT * FROM OnlineAgecy_brief')
	# now return the rendered template
	return render(request, "briefs/briefs_list.html", {'briefs': briefs})


@login_required(login_url="login/")
def brief_new(request):
    if request.method == "POST":
        form = BriefForm(request.POST)
        if form.is_valid():
            brief = form.save(commit=False)
            brief.save()
            return redirect('briefs')
    else:
        form = BriefForm()
    return render(request, 'layouts/form.html', {'form': form})


@login_required(login_url="login/")
def brief_detail(request, id):
    brief = get_object_or_404(Brief, id=id)
    return render(request, 'briefs/brief_detail.html', {'brief': brief})

@login_required(login_url="login/")
def brief_edit(request, id):
    brief = get_object_or_404(Brief, id=id)
    if request.method == "POST":
        form = BriefForm(request.POST, instance=brief)
        if form.is_valid():
            brief = form.save(commit=False)
            brief.save()
            return redirect('brief_detail', id=id)
    else:
        form = BriefForm(instance=brief)
    return render(request, 'layouts/form.html', {'form': form})

@login_required(login_url="login/")
def delete_brief(request, id):
    query = Brief.objects.get(id=id)
    query.delete()
    return redirect('briefs')

#--------------------Services Views------------------------------#
##################################################################

@login_required(login_url="login/")
def services(request):
    services = Service.objects.raw('SELECT * FROM OnlineAgecy_service')

    return render(request, "services/services_list.html", {'services': services})


@login_required(login_url="login/")
def services_new(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            services = form.save(commit=False)
            services.save()
            return redirect('services')
    else:
        form = ServiceForm()
    return render(request, 'layouts/form.html', {'form': form})


@login_required(login_url="login/")
def service_detail(request, id):
    service = get_object_or_404(Service, id=id)
    return render(request, 'services/service_detail.html', {'service': service})

@login_required(login_url="login/")
def service_edit(request, id):
    service = get_object_or_404(Service, id=id)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()
            return redirect('service_detail', id=id)
    else:
        form = ServiceForm(instance=service)
    return render(request, 'layouts/form.html', {'form': form})

@login_required(login_url="login/")
def service_all_clients(request, id):
	# get the blog clients that are published
	services = Contract.objects.raw('SELECT OnlineAgecy_contract.id, OnlineAgecy_contract_Services.contract_id AS id, Online_Agecy_service.id, Online_Agecy_service.Name, OnlineAgecy_contract_Services.service_id AS id'
                                    'from (OnlineAgecy_contract join OnlineAgecy_contract_Services using (id)) join OnlineAgecy_contract_Services using (id)')

    # 'SELECT OnlineAgecy_client.Name OnlineAgecy_service.Name AS ServiceName FROM OnlineAgecy_contract JOIN OnlineAgecy_client USING (id)')
    #SELECT table.id, other_table.name AS name from table join other_table using (id)
	return render(request, "services/allClientServices.html", {'services': services})


@login_required(login_url="login/")
def delete_service(request, id):
    query = Service.objects.get(id=id)
    query.delete()
    return redirect('services')


#--------------------contractors Views------------------------------#
#####################################################################


@login_required(login_url="login/")
def contractors(request):
    contractors = Contractor.objects.raw('SELECT * FROM OnlineAgecy_contractor')

    return render(request, "contractors/contractors_list.html", {'contractors': contractors})


@login_required(login_url="login/")
def contractors_new(request):
    if request.method == "POST":
        form = ContractorForm(request.POST)
        if form.is_valid():
            contractors = form.save(commit=False)
            contractors.save()
            return redirect('contractors')
    else:
        form = ContractorForm()
    return render(request, 'layouts/form.html', {'form': form})


@login_required(login_url="login/")
def contractor_detail(request, id):
    contractor = get_object_or_404(Contractor, id=id)
    return render(request, 'contractors/contractor_detail.html', {'contractor': contractor})

@login_required(login_url="login/")
def contractor_edit(request, id):
    contractor = get_object_or_404(Contractor, id=id)
    if request.method == "POST":
        form = ContractorForm(request.POST, instance=contractor)
        if form.is_valid():
            contractor = form.save(commit=False)
            contractor.save()
            return redirect('contractor_detail', id=id)
    else:
        form = ContractorForm(instance=contractor)
    return render(request, 'layouts/form.html', {'form': form})

def newest_contractors(request):
    items = Contractor.objects.raw('SELECT id ,Name FROM OnlineAgecy_contractor WHERE id NOT in(SELECT id AS Serv_id FROM OnlineAgecy_service '
                                   'WHERE NOT EXISTS (SELECT contract_id, service_id FROM OnlineAgecy_contract_Services '
                                   'WHERE OnlineAgecy_contract_Services.service_id = OnlineAgecy_service.id))')
    return render(request, 'contractors/new_contractors.html', {'items': items})

@login_required(login_url="login/")
def delete_contractor(request, id):
    query = Contractor.objects.get(id=id)
    query.delete()
    return redirect('contractors')

#--------------------Act Views------------------------------#
#####################################################################


@login_required(login_url="login/")
def acts(request):
    acts = Act.objects.raw('SELECT * FROM OnlineAgecy_act')

    return render(request, "acts/act_list.html", {'acts': acts})


@login_required(login_url="login/")
def act_new(request):
    if request.method == "POST":
        form = ActForm(request.POST)
        if form.is_valid():
            acts = form.save(commit=False)
            acts.save()
            return redirect('acts')
    else:
        form = ActForm()
    return render(request, 'layouts/form.html', {'form': form})


@login_required(login_url="login/")
def act_detail(request, id):
    act = get_object_or_404(Act, id=id)
    return render(request, 'acts/act_detail.html', {'act': act})

@login_required(login_url="login/")
def act_edit(request, id):
    act = get_object_or_404(Act, id=id)
    if request.method == "POST":
        form = ActForm(request.POST, instance=act)
        if form.is_valid():
            act = form.save(commit=False)
            act.save()
            return redirect('act_detail', id=id)
    else:
        form = ActForm(instance=act)
    return render(request, 'layouts/form.html', {'form': form})

@login_required(login_url="login/")
def delete_act(request, id):
    query = Act.objects.get(id=id)
    query.delete()
    return redirect('acts')
#--------------------Bill Views------------------------------#
#####################################################################


@login_required(login_url="login/")
def bills(request):
    bills = Bill.objects.raw('SELECT * FROM OnlineAgecy_bill')

    return render(request, "bills/bills_list.html", {'bills': bills})

def bills_new(request):
    if request.method == "POST":
        form = BillForm(request.POST)
        if form.is_valid():
            bills = form.save(commit=False)
            bills.save()
            return redirect('bills')
    else:
        form = BillForm()
    return render(request, 'layouts/form.html', {'form': form})

@login_required(login_url="login/")
def bills_detail(request, id):
    bill = get_object_or_404(Bill, id=id)
    return render(request, 'bills/bill_detail.html', {'bill': bill})

@login_required(login_url="login/")
def bills_edit(request, id):
    bill = get_object_or_404(Bill, id=id)
    if request.method == "POST":
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.save()
            return redirect('bills_detail', id=id)
    else:
        form = BillForm(instance=bill)
    return render(request, 'layouts/form.html', {'form': form})

@login_required(login_url="login/")
def delete_bill(request, id):
    query = Bill.objects.get(id=id)
    query.delete()
    return redirect('bills')
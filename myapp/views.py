from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from .forms import BootstrapAuthenticationForm, BootstrapPasswordChangeForm
from django.contrib import messages
from .models import PmList, CustomUser, PmReport, ChalanReport
from . import config, tools

def user_login(request):
    if request.method == 'POST':
        form = BootstrapAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = BootstrapAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = BootstrapPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = BootstrapPasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})

@login_required
def dashboard(request):
    if request.method == 'POST':
        userid = request.user.id
        pschache = request.POST['pschache']
        casechache = request.POST['casechache']
        CustomUser.objects.filter(id=userid).update(pschache=pschache, casechache=casechache)
        return redirect('/')
    else:
        pslist = config.pslist
        optlist = ['অপমৃত্যু', 'মামলা']
        activeps = request.user.pschache
        activelist = request.user.casechache
        context = ""
        if activeps:
            if activelist:
                context = PmList.objects.filter(referencePS=activeps, referenceType=activelist)
            else:
                context = PmList.objects.filter(referencePS=activeps)
        else:
            if activelist:
                context = PmList.objects.filter(referenceType=activelist)
            else:
                context = PmList.objects.all()
        return render(request, 'dashboard.html', {'context' : context, 'pslist' : pslist, 'optlist' : optlist})

@login_required
def insertnewpm(request):
    if request.method == 'POST':
        pmNo = request.POST['pmNo']
        pmdate = request.POST['pmdate']
        def get_two_digit_year(date_str):
            year = date_str[:4]  # extract the year from the date string
            two_digit_year = year[-2:]  # take the last two characters of the year
            return two_digit_year
        hospitalName = request.POST['hospitalName']
        uniquepmid = pmNo + "/" + get_two_digit_year(pmdate) + "/" + hospitalName
        doctorName = request.POST['doctorName']
        victimName = request.POST['victimName']
        referencePS = request.POST['referencePS']
        referenceType = request.POST['referenceType']
        referenceNo = request.POST['referenceNo']
        referenceDate = request.POST['referenceDate']
        referenceSection = request.POST['referenceSection']
        investofficer = request.POST['investofficer']
        caringcong = request.POST['caringcong']
        pmavailablity = request.POST.get('pmavailablity')
        pmstatus = request.POST.get('pmstatus')
        dnaavailablity = request.POST.get('dnaavailablity')
        dnastatus = request.POST.get('dnastatus')
        maavailablity = request.POST.get('maavailablity')
        mastatus = request.POST.get('mastatus')
        caavailablity = request.POST.get('caavailablity')
        castatus = request.POST.get('castatus')
        otheravailablity = request.POST.get('otheravailablity')
        otherstatus = request.POST.get('otherstatus')
        if PmList.objects.filter(uniquepmid = uniquepmid).exists():
            messages.error(request, 'এই পিএম নম্বরটি পূর্বে একবার এন্ট্রি দেওয়া আছে। ')
            return redirect('/')
        else:
            data = PmList(pmNo = pmNo, pmdate = pmdate, hospitalName = hospitalName, uniquepmid = uniquepmid, doctorName = doctorName, victimName = victimName, referencePS = referencePS, referenceType = referenceType, referenceNo = referenceNo, referenceDate = referenceDate, referenceSection = referenceSection, investofficer = investofficer, caringcong = caringcong, pmavailablity = pmavailablity, pmstatus = pmstatus, dnaavailablity = dnaavailablity, dnastatus = dnastatus, maavailablity = maavailablity, mastatus = mastatus, caavailablity = caavailablity, castatus = castatus, otheravailablity = otheravailablity, otherstatus = otherstatus)
            data.save()
            return redirect('/')
    else:
        hospital = config.hospital
        if request.user.is_superuser:
            pslist = config.pslist
        else:
            pslist = [request.user.psname]
        return render(request, 'insertpm.html', {'hospital':hospital, 'pslist':pslist})

@login_required
def editpm(request, id):
    if request.method == 'POST':
        pmNo = request.POST['pmNo']
        pmdate = request.POST['pmdate']
        def get_two_digit_year(date_str):
            year = date_str[:4]  # extract the year from the date string
            two_digit_year = year[-2:]  # take the last two characters of the year
            return two_digit_year
        hospitalName = request.POST['hospitalName']
        uniquepmid = pmNo + "/" + get_two_digit_year(pmdate) + "/" + hospitalName
        doctorName = request.POST['doctorName']
        victimName = request.POST['victimName']
        referencePS = request.POST['referencePS']
        referenceType = request.POST['referenceType']
        referenceNo = request.POST['referenceNo']
        referenceDate = request.POST['referenceDate']
        referenceSection = request.POST['referenceSection']
        investofficer = request.POST['investofficer']
        caringcong = request.POST['caringcong']
        pmavailablity = request.POST.get('pmavailablity')
        pmstatus = request.POST.get('pmstatus')
        dnaavailablity = request.POST.get('dnaavailablity')
        dnastatus = request.POST.get('dnastatus')
        maavailablity = request.POST.get('maavailablity')
        mastatus = request.POST.get('mastatus')
        caavailablity = request.POST.get('caavailablity')
        castatus = request.POST.get('castatus')
        otheravailablity = request.POST.get('otheravailablity')
        otherstatus = request.POST.get('otherstatus')
        PmList.objects.filter(id=id).update(pmNo = pmNo, pmdate = pmdate, hospitalName = hospitalName, uniquepmid = uniquepmid, doctorName = doctorName, victimName = victimName, referencePS = referencePS, referenceType = referenceType, referenceNo = referenceNo, referenceDate = referenceDate, referenceSection = referenceSection, investofficer = investofficer, caringcong = caringcong, pmavailablity = pmavailablity, pmstatus = pmstatus, dnaavailablity = dnaavailablity, dnastatus = dnastatus, maavailablity = maavailablity, mastatus = mastatus, caavailablity = caavailablity, castatus = castatus, otheravailablity = otheravailablity, otherstatus = otherstatus)
        return redirect('/')
    else:
        form = PmList.objects.get(id=id)
        hospital = config.hospital
        casetype = ['অপমৃত্যু', 'মামলা']
        if request.user.is_superuser:
            pslist = config.pslist
        else:
            pslist = [request.user.psname]
        return render(request, 'editpm.html', {'context':form, 'hospital':hospital, 'casetype':casetype, 'pslist':pslist})

@login_required
def ClosePM(request, id):
    if request.method == 'GET':
        PmList.objects.filter(id = id).delete()
        return redirect('/')

@login_required
def GeneratePMChalan(request):
    if request.method == 'POST':
        getMemo = tools.etob(str(request.POST['memo']))
        getDate = tools.etob(tools.dateformater(str(request.POST['date'])))
        getMonth = request.POST['month']
        tableData = PmList.objects.filter(pmstatus = 'no')
        loopcounter = 1
        context = '<html><head><title>Report</title><style>*{margin:0;padding:0;font-family:SolaimanLipi;font-size:18px;}</style></head><body>'
        context += '<p style="text-align:center;font-weight:bold;">গণপ্রজাতন্ত্রী বাংলাদেশ সরকার</p>'
        context += '<p style="text-align:center;">বাংলাদেশ পুলিশ</p>'
        context += '<p style="text-align:center;">অতিরিক্ত পুলিশ সুপারের কার্যালয়</p>'
        context += '<p style="text-align:center;">সাভার সার্কেল, ঢাকা</p><br/>'
        context += '<table style="width:100%;"><tr><td>স্মারক নং- সাভার সার্কেল/' + getMemo + '</td><td style="text-align:right;">তারিখ- ' + getDate + ' খ্রি.</td></tr></table><br/>'
        context += '<p>প্রতি</p>'
        context += '<p>&ensp;&ensp;&ensp;&ensp;অধ্যক্ষ</p>'
        context += '<p>&ensp;&ensp;&ensp;&ensp;শহীদ সোহরাওয়ার্দী মেডিকেল কলেজ হাসপাতাল</p>'
        context += '<p>&ensp;&ensp;&ensp;&ensp;শেরে বাংলা নগর, ঢাকা।</p><br/>'
        context += '<table><tr><td style="width:30px;vertical-align:top;">বিষয়:</td><td style="vertical-align:top;">' + getMonth + ' খ্রিঃ মাসে সাভার সার্কেলাধীন থানাসমূহের (সাভার, আশুলিয়া, ধামরাই) মুলতবি ' + tools.etob(str(tableData.count())) + ' টি মামলা/অপমৃত্যু মামলার ময়নাতদন্ত প্রতিবেদন প্রাপ্তির তাগিদপত্র প্রেরণ প্রসঙ্গে।</td></tr></table><br/>'
        context += '<p style="text-align:justify;">&ensp;&ensp;&ensp;&ensp;উপর্যুক্ত বিষয়ের প্রেক্ষিতে আপনার সদয় অবগতির জন্য জানানো যাচ্ছে যে, সাভার সার্কেলাধীন থানাসমূহের (সাভার, আশুলিয়া, ধামরাই) মুলতবি মামলা/অপমৃত্যু মামলাসমূহের ময়নাতদন্ত প্রতিবেদন প্রাপ্তির লক্ষ্যে ' + getMonth + ' খ্রিঃ মাসে ' + tools.etob(str(tableData.count())) + ' টি মামলা/অপমৃত্যু মামলার ময়নাতদন্ত প্রতিবেদন প্রাপ্তির তাগিদপত্র সংশ্লিষ্ট হাসপাতালে প্রেরণ করা হয়েছে। ইহা আপনার সদয় অবগতির জন্য প্রেরণ করা হলো।</p>'
        context += '<p style="text-align:center;font-weight:bold;">তালিকা:</p>'
        context += '<table style="width:100%;border-collapse:collapse;"><tr><th style="width:8%;border:1px solid black;font-size:14px;">ক্রমিক</th><th style="width:12%;border:1px solid black;font-size:14px;">মামলার সূত্র</th><th style="border:1px solid black;font-size:14px;">পিএম নং ও তাং</th><th style="border:1px solid black;font-size:14px;">ভিকটিমের নাম</th><th style="border:1px solid black;font-size:14px;">স্মারক নং ও তাং</th><th style="border:1px solid black;font-size:14px;">তাগিদ নং</th><th style="border:1px solid black;font-size:14px;">ডাক্তারের নাম</th></tr>'
        for data in tableData:
            context += '<tr><td style="border:1px solid black;text-align:center;font-size:14px;">' + tools.etob(str(loopcounter)) + '.</td>'

            context += '<td style="border:1px solid black;font-size:14px;padding-left:5px;padding-right:5px;text-align:justify;">' + data.referencePS + ' থানার ' + data.referenceType + ' নং- ' + tools.etob(str(data.referenceNo)) + ', তারিখ- ' + tools.etob(tools.dateformater(str(data.referenceDate))) + ' খ্রি.'
            if data.referenceSection != '':
                context += ', ধারা- ' + data.referenceSection
            
            context += '</td><td style="border:1px solid black;font-size:14px;text-align:justify;">পিএম নং- '+ tools.etob(str(data.pmNo)) + ', তারিখ- ' + tools.etob(tools.dateformater(str(data.pmdate))) + ' খ্রি.</td><td style="border:1px solid black;font-size:14px;text-align:center;">'

            if data.victimName != '':
                context += data.victimName

            context += '</td><td style="border:1px solid black;font-size:14px;text-align:justify;">স্মারক নং- ' + tools.etob(str(data.lastMemoNo)) + ', তারিখ- ' + tools.etob(tools.dateformater(str(data.lastMemoDate))) + ' খ্রি.'
            
            context += '</td><td style="border:1px solid black;font-size:14px;text-align:center;">' 
            if data.reminderNo != '':
                context += tools.etob(str(data.reminderNo))
            context += '</td><td style="border:1px solid black;font-size:14px;padding-left:5px;padding-right:5px;text-align:center;">'
            
            if data.doctorName is not None:
                context += data.doctorName

            context += '</td></tr>'
            loopcounter += 1
        context += '</table><br/>'
        context += '<br/><br/><table style="width:100%;"><tr><td style="width:75%;"></td><td style="text-align:center;">শাহিদুল ইসলাম<br/>বিপি-৮৭১৩১৫৯৩৮৭<br/>অতিরিক্ত পুলিশ সুপার<br/>সাভার সার্কেল, ঢাকা</td></tr></table><br/>'
        context += '<table style="width:100%;"><tr><td>স্মারক নং- সাভার সার্কেল/' + getMemo + '</td><td style="text-align:right;">তারিখ- ' + getDate + ' খ্রি.</td></tr></table><br/>'
        context += '<p style="font-weight:bold;">অনুলিপি সদয় অবগতির জন্য প্রেরণ করা হলো:</p>'
        context += '<p>&emsp;&emsp;১. ডিআইজি, ঢাকা রেঞ্জ, বাংলাদেশ পুলিশ, ঢাকা</p>'
        context += '<p>&emsp;&emsp;২. পুলিশ সুপার, ঢাকা জেলা</p>'
        context += '<p>&emsp;&emsp;৩. অফিস কপি</p><br/>'
        context += '<br/><br/><table style="width:100%;"><tr><td style="width:75%;"></td><td style="text-align:center;">শাহিদুল ইসলাম<br/>বিপি-৮৭১৩১৫৯৩৮৭<br/>অতিরিক্ত পুলিশ সুপার<br/>সাভার সার্কেল, ঢাকা</td></tr></table>'
        finalData = ChalanReport(chalanReport=context)
        finalData.save()
        return redirect('/')
    else:
        return render(request, 'generatePMChalan.html')

@login_required
def GeneratePMReport(request):
    if request.method == 'POST':
        getMemo = int(request.POST['memo'])
        getDate = request.POST['date']
        getPendingList = PmList.objects.filter(pmstatus = 'no')
        context = '<html><head><title>Report</title><style>*{margin:0;padding:0;font-family:SolaimanLipi;font-size:18px;}</style></head><body>'
        for value in getPendingList:
            if value.reminderNo != 0:
                context += '<p style="text-align:right;font-weight:bold;position:relative;top:18px;">তাগিদপত্র- ' + tools.etob(str(value.reminderNo)) + '</p>'
            context += '<p style="text-align:center;font-weight:bold;">গণপ্রজাতন্ত্রী বাংলাদেশ সরকার</p>'
            context += '<p style="text-align:center;">বাংলাদেশ পুলিশ</p>'
            context += '<p style="text-align:center;">অতিরিক্ত পুলিশ সুপারের কার্যালয়</p>'
            context += '<p style="text-align:center;">সাভার সার্কেল, ঢাকা</p><br/>'
            context += '<table style="width:100%;"><tr><td>স্মারক নং- সাভার সার্কেল/' + tools.etob(str(getMemo)) + '(৪)/১' + '</td><td style="text-align:right;">তারিখ- ' + tools.etob(tools.dateformater(str(getDate))) + ' খ্রি.</td></tr></table><br/>'
            if value.reminderNo == 0:
                context += '<p>সূত্র:&ensp;&nbsp;১. ' + value.referencePS + ' থানার ' + value.referenceType + ' নং- ' + tools.etob(str(value.referenceNo)) + ', তারিখ- ' + tools.etob(tools.dateformater(str(value.referenceDate))) + ' খ্রি.'
                if value.referenceSection != '':
                    context += ', ধারা- ' + value.referenceSection
                context += ', (ভিকটিম: ' + value.victimName + ')'
                context += '</p>'
                context += '<p>&emsp;&emsp;২. পিএম নং- ' + tools.etob(str(value.pmNo)) + ', তারিখ- ' + tools.etob(tools.dateformater(str(value.pmdate))) + ' খ্রি.'
                if value.doctorName != '':
                    context += ' (ডাক্তার: ' + value.doctorName + ')'
                context += '</p><br/>'
                context += '<p style="font-weight:bold;">বিষয়: ময়নাতদন্ত প্রতিবেদন প্রেরণ প্রসঙ্গে।</p><br/>'
                context += '<p style="text-align:justify;">&emsp;&emsp;উপর্যুক্ত বিষয়ের প্রেক্ষিতে আপনার সদয় অবগতির জন্য জানানো যাচ্ছে যে, সূত্রে বর্ণিত ' + value.referenceType + 'র মরদেহ আপনার প্রতিষ্ঠানে ময়নাতদন্তের জন্য প্রেরণ করা হয়। ময়নাতদন্ত প্রতিবেদন ফৌজদারী বিচার ব্যবস্থায় ন্যায়বিচার প্রতিষ্ঠায় অতি গুরুত্বপূর্ণ একটি দলিল। বিশেষত হত্যা মামলা বা নিহত ব্যক্তির জীবনাবসানে কারো অপরাধজনক দায়বদ্ধতা (Criminal Liabilities) আছে কি না তা তদন্তের শুরুতে জানা এবং সে অনুযায়ী পুলিশি কার্যক্রম সম্পন্ন করে সঠিক পুলিশ রিপোর্ট দাখিলের জন্য অনুরূপ প্রতিবেদন যথাসময়ে প্রাপ্তি জরুরী। কিন্তু অদ্যাবধি উক্ত ' + value.referenceType + 'র ময়নাতদন্ত প্রতিবেদন পাওয়া যায়নি। <br/><br/>&emsp;&emsp;এমতাবস্থায় বর্ণিত ' + value.referenceType + 'র ভিকটিমের মরদেহের ময়নাতদন্ত প্রতিবেদন দ্রুত প্রেরণের জন্য আপনাকে বিশেষভাবে অনুরোধ করা হলো।</p><br/>'
            else:
                context += '<p>সূত্র:&ensp;&nbsp;অতিঃ পুলিশ সুপারের কার্যালয়, সাভার সার্কেল, ঢাকার স্মারক নং- ' + tools.etob(str(value.lastMemoNo)) + ', তাং- ' + tools.etob(tools.dateformater(str(value.lastMemoDate))) + ' খ্রি.</p><br/>'
                context += '<p style="font-weight:bold;">বিষয়: ময়নাতদন্ত প্রতিবেদন প্রেরণ প্রসঙ্গে।</p><br/>'
                context += '<p style="text-align:justify;">&emsp;&emsp;উপর্যুক্ত বিষয়ে সূত্রোক্ত স্মারক মোতাবেক ' + value.referencePS + ' থানার ' + value.referenceType + ' নং- ' + tools.etob(str(value.referenceNo)) + ', তারিখ- ' + tools.etob(tools.dateformater(str(value.referenceDate))) + ' খ্রি.'
                if value.referenceSection != '':
                    context += ' ধারা- ' + value.referenceSection
                context += ' (ভিকটিম: ' + value.victimName + ')'    
                context += ', পিএম নং- ' + tools.etob(str(value.pmNo)) + ', তারিখ- ' + tools.etob(tools.dateformater(str(value.pmdate))) + ' খ্রি.'
                if value.doctorName != '':
                    context += ' (ডাক্তার: ' + value.doctorName + ')'
                context += ' এর বরাতে দ্রুত ময়নাতদন্ত প্রতিবেদন প্রাপ্তির নিমিত্ত্বে অনুরোধ সংবলিত পত্র প্রেরণ করা হয়েছিল। কিন্তু অদ্যাবধি উল্লিখিত ' + value.referenceType + 'র ময়নাতদন্ত প্রতিবেদন পাওয়া যায়নি। ফলে দ্রুত তদন্ত সমাপ্তি, রহস্য উদঘাটন ও অপরাধী চিহ্নিতকরণসহ তদন্তকার্যে বিঘ্ন ঘটছে। <br/><br/>&emsp;&emsp;এই প্রসঙ্গে পুলিশ রেগুলেশন্স বেঙ্গল, ১৯৪৩ এর প্রবিধান নং- ৩০৬(ক) প্রবিধানটি উল্লেখ্য। উল্লিখিত প্রবিধানে নির্দেশিত আছে যে, “ময়নাতদন্ত সমাপ্ত হওয়ার সাথে সাথে মেডিকেল অফিসার নির্ধারিত ফরম-এ তিন কপি প্রতিবেদন প্রস্তুত করবেন। একটি কার্বন কপি তিনি মরদেহ বহন করে আনা কনস্টেবলকে দেবেন, মূল প্রতিবেদন চালান ও সুরতহাল প্রতিবেদনসহ প্রযোজ্য ক্ষেত্রে সিভিল সার্জনের অগ্রায়নের মাধ্যমে পুলিশ সুপারের নিকট প্রেরণ করবেন এবং তৃতীয় কার্বন কপিটি মেডিকেল অফিসারের নিকট রক্ষিত রেজিস্টারে সংযুক্ত করে রাখবেন”। <br/><br/>&emsp;&emsp;বর্ণিতাবস্থায়, যথাসময়ে ময়নাতদন্ত প্রতিবেদন প্রাপ্তির জন্য আপনার সদয় সহযোগিতা ও প্রযোজ্য ক্ষেত্রে প্রয়োজনীয় নির্দেশনা প্রদানের জন্য পুনরায় অনুরোধ করছি।</p>'
                
            context += '<br/><br/><table style="width:100%;"><tr><td style="width:75%;"></td><td style="text-align:center;">' + tools.etob(tools.dateformater(str(getDate))) + '<br/>শাহিদুল ইসলাম<br/>বিপি-৮৭১৩১৫৯৩৮৭<br/>অতিরিক্ত পুলিশ সুপার<br/>সাভার সার্কেল, ঢাকা</td></tr></table>'
            context += '<p style="font-weight:bold;">কার্যার্থে:</p>'
            context += '<p>&emsp;&emsp;বিভাগীয় প্রধান, ফরেনসিক মেডিসিন বিভাগ</p>'
            context += '<p>&emsp;&emsp;' + value.hospitalName + '</p><br/>'
            context += '<p style="font-weight:bold;">জ্ঞাতার্থে:</p>'
            context += '<p>&emsp;&emsp;১. ডিআইজি, ঢাকা রেঞ্জ, বাংলাদেশ পুলিশ, ঢাকা</p>'
            context += '<p>&emsp;&emsp;২. পুলিশ সুপার, ঢাকা জেলা</p>'
            context += '<p style="page-break-after:always;">&emsp;&emsp;৩. অধ্যক্ষ, ' + value.hospitalName + '</p>'
            PmList.objects.filter(id = value.id).update(reminderNo = value.reminderNo + 1, lastMemoNo = getMemo, lastMemoDate = getDate)
            getMemo += 1
        context += '</body></html>'
        finalData = PmReport(pmReport=context)
        finalData.save()
        return redirect('/')
    else:
        return render(request, 'generatePM.html')

@login_required
def Archive(request):
    if request.method == 'GET':
        dataChalan = ChalanReport.objects.all()
        dataPM = PmReport.objects.all()
        return render(request, 'archive.html', {
            'contextPM':dataPM, 
            'contextChalan':dataChalan
        })

@login_required
def ViewReport(request, tbl, id):
    if request.method == 'GET':
        if tbl == 'tagid':
            data = PmReport.objects.get(id=id)
            context = data.pmReport
        elif tbl == 'chalan':
            data = ChalanReport.objects.get(id=id)
            context = data.chalanReport
        return HttpResponse(context)

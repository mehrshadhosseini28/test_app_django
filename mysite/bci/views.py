from django.shortcuts import render, get_list_or_404

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.urls import reverse
import json
import requests
import os
import subprocess
import sys
from threading import Thread 
from .models import ProccesDetails

def my_func(procces_detail_id):
    import bci_lib as bl
    pdi = ProccesDetails.objects.get(id=procces_detail_id)
    bl.Dataset.change_BASE_LOCAL_LOCATION('/workspace/')

    pipeline = bl.SingleRun()
    load1 = pipeline.add_stage(bl.Stages.LoadData.LoadFromDataset)
    load1.set_params(getattr(bl.Dataset.Cho2017,pdi.patient))

    rtw1 = pipeline.add_stage(bl.Stages.Preprocess.RawDataToEpochsData)
    rtw1.set_params()

    band1 = pipeline.add_stage(bl.Stages.Preprocess.BandPassFilter)
    band1.set_params(pdi.filter_low, pdi.filter_high)

    split1 = pipeline.add_stage(bl.Stages.Preprocess.TestTrainSplit)
    split1.set_params(test_size=pdi.split_persent/100, random_state=1)

    psd1 = pipeline.add_stage(bl.Stages.FeatureExtraction.PSD)
    psd1.set_params(eval(pdi.psd_freq))

    model1 = pipeline.add_stage(bl.Stages.Classification.CreateModel)
    model1.set_params(bl.Stages.Classification.MLModel.SVM.SVC)

    train1 = pipeline.add_stage(bl.Stages.Classification.Train)
    train1.set_params()

    test1 = pipeline.add_stage(bl.Stages.Classification.Test)
    test1.set_params('accuracy')

    pipeline.do_task()

    # print('database:\n', pipeline._database.get_database_dict())
    print('---------------\nfinal result:\n',pipeline._database.get(test1._outputs[0])[0].result)

    pdi.result_acc = pipeline._database.get(test1._outputs[0])[0].result
    pdi.save()

@csrf_exempt
def create_and_start(request):
    """
    POST API: Create and Start a proccess
    Data: JSON
        patient = str,
        filter_low = float,
        filter_high = float,
        psd_freq = str --> example: "[(1,2), (3,4)]",
        split_persent = float,
        svm_c = float,
        svm_l1 = float,
        svm_l2 = float
    Response: JSON
        pid: int
    """
    if request.method == "POST":
        DATA = json.loads(request.body)
        p = ProccesDetails.objects.create(**DATA)
        t = Thread(target = my_func, args =(p.id, )) 
        t.start()
        response_data = {
            "success": True,
            'pid': p.id
        }
    else:
        response_data = {
            "success": False,
            "massege": "use this API with POST method"
        }
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def check_acc(request):
    """
    GET API:
    Data: JSON
        pid = int
    Response: JSON
        "result_acc": float or None
    """
    pid = request.GET.get('pid', None)
    if pid is None:
        response_data = {"success": False, "massege": "error1"}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    try:
        p = ProccesDetails.objects.get(id=pid)
        response_data = {"success": True, "result_acc": p.result_acc}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
    except Exception:
        response_data = {"success": False, "massege": "error2"}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
        

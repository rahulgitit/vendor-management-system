from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .metrics import update_vendor_metrics




class VendorViewSet(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
#vendors/{vendor_id}/performance/
    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        # vendor= self.get_object()
        # # update_vendor_metrics(vendor)
        # print(vendor)
        try:
            vendor=Vendor.objects.get(pk=pk)
            performance=HistoricalPerformance.objects.filter(vendor=vendor)
            per_seializers=HistoricalPerformanceSerializer(performance,many=True, context={"request":request})
            return Response(per_seializers.data)
        except Exception as e:
            print(e)
            return Response({
                'message':'Company might not exists !! Error'
            })
    # @action(detail=True, methods=['get'])
    # def performance(self, request, pk=None):
    #     vendor = self.get_object()
    #     update_vendor_metrics(vendor)
    #     return Response({
    #         'on_time_delivery_rate': vendor.on_time_delivery_rate,
    #         'quality_rating_avg': vendor.quality_rating_avg,
    #         'average_response_time': vendor.average_response_time,
    #         'fulfillment_rate': vendor.fulfillment_rate
    #     })

            

class PurchaseOrderViewSet(ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    # def perform_create(self,request,vendor):
    #     po = HistoricalPerformanceSerializer.save()
    #     print(po)
    #     update_vendor_metrics(vendor.po)

    # def perform_update(self,request,vendor):
    #     po = HistoricalPerformanceSerializer.save()
    #     update_vendor_metrics(vendor.po)

class HistoricalPerformanceViewSet(ModelViewSet):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
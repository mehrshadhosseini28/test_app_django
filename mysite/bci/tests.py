from django.test import TestCase
from .models import Category, Product, Shop
from .views import get_duration, select_items_for_paging, next_page, prev_page
from .views import category_list
from django.urls import reverse
from django.utils import timezone
import datetime


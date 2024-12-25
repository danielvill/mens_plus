from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.venta import Venta
from pymongo import MongoClient
db = dbase()

venta = Blueprint('venta', __name__)


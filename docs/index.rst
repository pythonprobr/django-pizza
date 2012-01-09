=========================
Django's Pizza
=========================

Introdução rápida ao Django

* Luciano Ramalho, Academia Python / Globalcode

* luciano@ramalho.org

----------------
O que é Django
----------------

- um framework

  - um conjunto integrado de componentes e convenções
  
- ágil

  - com pouco código, obtemos muita funcionalidade
  
- para aplicações web

  - templates, validação de formulários, autenticação etc.
  
- baseadas em banco de dados

  - integra-se com PostgreSQL, MySQL, Oracle e SQLite
  
---------------
Nosso exemplo
---------------

- sistema para uma pizzaria que entrega em casa

  - registro e busca de clientes pelo telefone
  
  - registro de pedidos
  
  - controle da produção
  
  - controle das entregas
  
--------------
Para começar
--------------

- criar aplicação::

  $ django-admin.py startproject pizza
  
- resultado::

    pizza/
        __init__.py
        manage.py
        settings.py
        urls.py

---------------------------
Ajustes no ``settings.py``
---------------------------

Para usar o SQLite::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'pizzaria.sqlite3',      # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
  
Para usar o PostgreSQL::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'pizzaria',              # Or path to database file if using sqlite3.
            'USER': 'dante',                 # Not used with sqlite3.
            'PASSWORD': 'com3d1a',           # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

----------------------------------
Outros ajustes no ``settings.py``
----------------------------------

::

    # coding: utf-8

- especificar na 1ª linha a codificação do arquivo-fonte ``settings.py``

  - necessário para usar acentação, mesmo que apenas em comentários

::

    TIME_ZONE = 'America/Sao_Paulo'

- fuso horário para exibição de datas e horas

  - no Windows, precisa ser igual ao fuso do servidor

::

    LANGUAGE_CODE = 'pt-br'

- idioma da mensagens (admin, validação etc)

::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.admin',     # <- Django Admin
        'django.contrib.admindocs', # <- documentação local
    )
    
- aplicativos instalados: instalar ``admin`` e ``admin_docs``


-------------------------
Ajustes no ``urls.py``
-------------------------

"Descomentar" linhas para habilitar ``admin/`` e ``admin/doc/``

::

    from django.conf.urls.defaults import *
    
    from django.contrib import admin
    admin.autodiscover()
    
    urlpatterns = patterns('',
        # Example:
        # (r'^pizza/', include('pizza.foo.urls')),
    
        (r'^admin/doc/', include('django.contrib.admindocs.urls')), # <-
    
        (r'^admin/(.*)', admin.site.root), # <-
    )


---------------------------------------------
Criar tabelas de autenticação e configuração
---------------------------------------------

::

    $ ./manage.py syncdb   
    Creating table auth_permission
    Creating table auth_group
    Creating table auth_user
    Creating table auth_message
    Creating table django_content_type
    Creating table django_session
    Creating table django_site
    Creating table django_admin_log
    
    You just installed Django's auth system, which means you don't have any superusers defined.
    Would you like to create one now? (yes/no): yes
    Username (Leave blank to use 'luciano'): admin
    E-mail address: a@b.cd
    Password: 
    Password (again): 
    Superuser created successfully.
    Installing index for auth.Permission model
    Installing index for auth.Message model
    Installing index for admin.LogEntry model
    $ 

---------------------------------
Criar o modelo de cliente
---------------------------------

- iniciar a aplicação ``entrega``::

    $ ./manage.py startapp entrega
    
- resultado::

    pizza/
        __init__.py
        manage.py
        settings.py
        urls.py
        entrega/
            __init__.py
            models.py
            views.py

---------------------------------
``models.py``: um exemplo
---------------------------------

- definições de modelos de dados vão em ``entrega/models.py``

::

    from django.db import models
    
    class Cliente(models.Model):
        fone = models.CharField(max_length=16, db_index=True)
        ramal = models.CharField(max_length=4, blank=True, db_index=True)
        contato = models.CharField(max_length=64, db_index=True)
        outros_contatos = models.TextField(blank=True)
        logradouro = models.CharField(max_length=32)
        numero = models.PositiveIntegerField(u'número')
        complemento = models.CharField(max_length=32, blank=True)
        obs = models.TextField(blank=True)
        
        class Meta:
            unique_together = ['fone', 'ramal']
            
---------------------------------
``views.py``: um exemplo
---------------------------------

::

    from django.shortcuts import render_to_response
    from entrega.models import Pizza
    from django.http import Http404    

    def listar_pizzas(request):
        pizzas = Pizza.objects.all()
        template_vars = {'pizzas':pizzas}
        return render_to_response('entrega/preparo.html', template_vars)

    def cliente(request, fone):
        res = Pizza.objects.filter(fone=fone)
        qt = res.count()
        if qt == 0:
            raise Http404()
        elif qt == 1:
            return render_to_response('clientes/ficha.html', {'cliente': res[0]})
        else:
            return render_to_response('clientes/lista.html', {'clientes': res})
       
    

--------------------------------------
Primeira versão do modelo de cliente
--------------------------------------

::

    from django.db import models
    
    class Cliente(models.Model):
        fone = models.CharField(max_length=16)
        ramal = models.CharField(max_length=4, blank=True)
        contato = models.CharField(max_length=64)
        logradouro = models.CharField(max_length=32)
        numero = models.PositiveIntegerField(u'número')
        complemento = models.CharField(max_length=32, blank=True)
        
        class Meta:
            unique_together = ['fone', 'ramal']
            
            
.. code-block:: sql

    CREATE TABLE "entrega_cliente" (
        "id" serial NOT NULL PRIMARY KEY,
        "fone" varchar(8) NOT NULL,
        "ramal" varchar(4) NOT NULL,
        "contato" varchar(64) NOT NULL,
        "logradouro" varchar(32) NOT NULL,
        "numero" integer CHECK ("numero" >= 0) NOT NULL,
        "complemento" varchar(32) NOT NULL,
        UNIQUE ("ddd", "fone", "ramal")
    )



---------------------------------
Alguns exemplos de campos
---------------------------------

- ``CharField``

::

    ramal = models.CharField(max_length=4, blank=True)



.. code-block:: sql

    "ramal" varchar(4) NOT NULL,
    


- ``PositiveIntegerField``

::

    numero = models.PositiveIntegerField(u'número')



.. code-block:: sql

    "numero" integer CHECK ("numero" >= 0) NOT NULL,
    

-------------------------------------
Criar tabela ``cliente``
-------------------------------------

- instalar nossa aplicação::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.admin',
        'django.contrib.admindocs',
        'pizza.entrega',   # <- nova linha
    )


- criar tabela ``cliente``::

    $ ./manage.py syncdb   

- ``syncdb`` limita-se a criar novas tabelas
  
  - nunca altera tabelas existentes
  
- para alterar tabelas existentes, é preciso apagá-las::

    $ ./manage.py reset entrega  


---------------------------------------------
Conectar o modelo à interface administrativa
---------------------------------------------

- criar arquivo ``entrega/admin.py`` para registrar modelos que devem ser manipulados via admin::

    from django.contrib import admin
    from pizza.entrega.models import Cliente
    
    admin.site.register(Cliente)


-----------------------------------------------
Melhorar a apresentação das listas de clientes
-----------------------------------------------

- em Python, os métodos ``__str__`` e ``__unicode__`` definem a forma padrão de exibição de um objeto

  - para evitar problemas com acentuação, prefira sempre o ``__unicode__``
  
  - note que as constantes são Unicode também (``u'abc'``)

- arquivo ``entrega/models.py``::

    class Cliente(models.Model):
    
        # ... campos ...    
    
        def __unicode__(self):
            fone = self.fone
            if self.ddd != DDD_DEFAULT:
                fone = u'(%s)%s' % (self.ddd, fone)
            if self.ramal:
                fone += ' r.' + self.ramal
            return u'%s - %s' % (fone, self.contato)



-------------------------------------------------
Customizar administração de clientes
-------------------------------------------------


- arquivo ``entrega/admin.py``::

    from django.contrib import admin
    from pizza.entrega.models import Cliente
    
    class ClienteAdmin(admin.ModelAdmin):
        list_display = ('fone', 'contato', 'endereco')
        list_display_links = ('fone', 'contato')
        search_fields = ('fone', 'contato', 'logradouro', 'numero')
    
    admin.site.register(Cliente, ClienteAdmin)
    

- ``list_display``: campos exibidos em colunas na listagem

- ``list_display_links``: campos com links na listagem

- ``search_fields``: campos onde será feita a buscasa

-------------------------------------------------
Customizar administração de clientes 2
-------------------------------------------------

- ``list_display`` pode incluir métodos, além de campos 

- arquivo ``entrega/models.py``::

    def endereco(self):
        end = u'%s, %s' % (self.logradouro, self.numero)
        if self.complemento:
            end += u', ' + self.complemento
        return end
    endereco.short_description = u'endereço'

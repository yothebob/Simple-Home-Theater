import core.settings as settings


#run this file to run the program of your choice
if settings.DEPLOYMENT_TYPE == "CLI":
    import cli.main
elif settings.DEPLOYMENT_TYPE == "WEB":
    import webapp.main

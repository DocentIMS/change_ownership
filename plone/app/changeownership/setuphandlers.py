from plone.app.changeownership import logger
from Products.CMFCore.utils import getToolByName


def migrateTo1000(context):
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-plone.app.changeownership:default')
    logger.info("Migrated to version 0.5")


def migrateTo2000(context):
    """Re-import the control panel so existing sites pick up the
    Plone 6 Bootstrap-icons configlet icon.
    """
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(
        'profile-plone.app.changeownership:default', 'controlpanel')
    logger.info("Migrated to version 2.0")

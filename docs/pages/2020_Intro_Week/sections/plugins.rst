.. _2020_virtual_intro:plugins:

***************************************************
Interfacing with external codes and writing plugins
***************************************************

This session is meant to get you started with writing your first AiiDA plugin.

If you haven't done so already, please **first** watch the `introduction to the AiiDA plugin system <https://www.youtube.com/watch?v=wQx0eRfBSzM&list=PL19kfLn4sO_-QtPaHAA8KByFluT2vvlG0>`_ (~20 minutes).

For this session, we suggest two options depending on your interests -- please post in the chat which of the two (A/B) you are going to follow:


 A. **Goal:** You would like to learn how to interface AiiDA with external codes using a fully worked example (level: *medium*).

    **Task:** Follow the tutorial on `How to run external codes <https://aiida.readthedocs.io/projects/aiida-core/en/latest/howto/codes.html>`_.

    **Result:** You will write a Python script with your first `CalcJob` and `Parser` plugin, telling AiiDA how to write inputs and parse outputs for a simple external executable.

    **Time:** This should be easily doable in the available 1.5h.

 B. **Goal:** You have a specific external code that you would like to interface with AiiDA (level: *advanced*).

    **Task:** Template your own plugin package using the `AiiDA plugin cutter <https://github.com/aiidateam/aiida-plugin-cutter>`_ and start wrapping your code.

    **Result:** An AiiDA plugin package, prepared for distribution via PyPI, and including templates for continuous integration tests and documentation. 

    **Time:** Don't expect to have a fully fledged plugin ready by the end of the session! 
    This is is an open-ended task aimed at getting you through initial hurdles more quickly by having AiiDA developers around to ask for help.


Useful resources for task B
---------------------------

 * Guidelines on plugin design
 * Documentation on `how to package plugins <https://aiida.readthedocs.io/projects/aiida-core/en/latest/howto/plugins.html>`_
 * Rundown of `repository contents of the aiida-diff package <https://github.com/aiidateam/aiida-diff#repository-contents>`_ (the default output of the plugin cutter)

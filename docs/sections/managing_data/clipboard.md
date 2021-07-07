Type strings can be used to class certain types of data, for example here we have general groups (`core`), groups containing pseudopotentials (`core.upf`), and an auto-generated group containing the nodes we imported from the archive (`core.import`).
For advanced use, you can create your own group type plugins, with specialised methods by sub-classing the general `Group` class.

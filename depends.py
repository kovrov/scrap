#!/usr/bin/env python

SOLUTION_DIR = "c:/home/projects/twin"
CONFIG_NAME = "Release|Win32"


import sys, os, re
import xml.etree.ElementTree as ElementTree


class Project():
	
	#macro_pattern = re.compile(r'\$\(\w+\)')
	def __init__(self, path):
		tree = ElementTree.parse(path)
		projtree = tree.getroot()
		self.name = projtree.attrib["Name"]
		self.macros = {
				"ProjectName" : projtree.attrib["Name"],
				"TargetName" : projtree.attrib["Name"],
				# this is shortcuts
				"ConfigurationName" : "",
				"DevEnvDir" : "",
				"FrameworkDir" : "",
				"FrameworkSDKDir" : "",
				"FrameworkVersion" : "",
				"FxCopDir" : "",
				"Inherit" : "",
				"InputDir" : "",
				"InputExt" : "",
				"InputFileName" : "",
				"InputName" : "",
				"InputPath" : "",
				"IntDir" : "",
				"NoInherit" : "",
				"OutDir" : "",
				"ParentName" : "",
				"PlatformName" : "",
				"ProjectDir" : "",
				"ProjectExt" : "",
				"ProjectFileName" : "",
				"ProjectPath" : "",
				"References" : "",
				"RemoteMachine" : "",
				"RootNameSpace" : "",
				"SafeInputName" : "",
				"SafeParentName" : "",
				"SafeRootNamespace" : "",
				"SolutionDir" : "",
				"SolutionExt" : "",
				"SolutionFileName" : "",
				"SolutionName" : "",
				"SolutionPath" : "",
				"StopEvaluating" : "",
				"TargetDir" : "",
				"TargetExt" : "",
				"TargetFileName" : "",
				"TargetPath" : "",
				"VCInstallDir" : "",
				"VSInstallDir" : "",
				"WebDeployPath" : "",
				"WebDeployRoot" : ""}
		self.dependencies = self.get_project_dependencies(projtree, CONFIG_NAME)
		self.produces = [self.get_project_library(projtree, CONFIG_NAME)]


	def get_project_dependencies(self, projtree, config):
		for conf in projtree.findall("Configurations/Configuration"):
			if conf.attrib["Name"] == config:
				for tool in conf.findall("Tool"):
					if tool.attrib["Name"] == "VCLinkerTool" or tool.attrib["Name"] == "VCLibrarianTool":
						if tool.attrib.has_key("AdditionalDependencies"):
							return [lib.lower() for lib in tool.attrib["AdditionalDependencies"].split()]
						break
				break
		return []


	def get_project_library(self, projtree, config):
		for conf in projtree.findall("Configurations/Configuration"):
			if conf.attrib["Name"] == config:
				for tool in conf.findall("Tool"):
					if tool.attrib["Name"] == "VCLinkerTool":
						if tool.attrib.has_key("ImportLibrary"): lib = tool.attrib["ImportLibrary"]
						else: lib = "$(TargetDir)$(TargetName).lib"
						return re.sub('\$\((\w+)\)', self.__re_sub_callback, lib).strip('\\/').lower()
					if tool.attrib["Name"] == "VCLibrarianTool":
						if tool.attrib.has_key("OutputFile"): lib = tool.attrib["OutputFile"]
						else: lib = "$(OutDir)\$(ProjectName).lib"
						return re.sub('\$\((\w+)\)', self.__re_sub_callback, lib).strip('\\/').lower()
				break


	def __re_sub_callback(self, match):
		if match.group(1) in self.macros:
			return self.macros[match.group(1)]
		else: return match.group(0)


def get_projects(path):
	projects = []
	for root, dirs, files in os.walk(path, topdown=False):
		for name in files:
			p = os.path.join(root, name)
			(r, ext) = os.path.splitext(p)
			if ext == ".vcproj":
				projects.append(p)
	return projects


if __name__ == '__main__':
	projects = {}
	libs = {}
	proj_paths = [os.path.normpath(project) for project in get_projects(SOLUTION_DIR) if project.lower().rfind("test") == -1]
	for project_path in proj_paths:
		project = Project(project_path)
		projects[project.name] = project
		for lib in project.produces:
			libs[lib] = project
	for k, project in projects.iteritems():
		print project.name
		for lib in project.dependencies:
			if libs.has_key(lib):
				print "", libs[lib].name
			else:
				print "", lib, "(external)"

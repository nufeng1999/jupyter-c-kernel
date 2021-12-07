from typing import Dict, Tuple, Sequence,List
from plugins.ISpecialID import IStag,IDtag,IBtag,ITag
from plugins._filter2_magics import Magics
import os
class MyInclude(IStag):
    kobj=None
    def getName(self) -> str:
        # self.kobj._write_to_stdout("setKernelobj setKernelobj setKernelobj\n")
        return 'MyInclude'
    def getAuthor(self) -> str:
        return 'Author'
    def getIntroduction(self) -> str:
        return 'MyInclude'
    def getPriority(self)->int:
        return 0
    def getExcludeID(self)->List[str]:
        return []
    def getIDSptag(self) -> List[str]:
        return ['include']
    def setKernelobj(self,obj):
        self.kobj=obj
        # self.kobj._write_to_stdout("setKernelobj setKernelobj setKernelobj\n")
        return
    def on_shutdown(self, restart):
        return
    def on_ISpCodescanning(self,key, value,magics,line) -> str:
        # self.kobj._write_to_stdout(line+" on_ISpCodescanning\n")
        self.kobj.addkey2dict(magics,'include')
        return self.includehander(self,key, value,magics,line)
    def on_Codescanning(self,magics,code)->Tuple[bool,str]:
        pass
        return False,code
    def on_before_buildfile(self,code,magics)->Tuple[bool,str]:
        return False,''
    def on_after_buildfile(self,returncode,srcfile,magics)->bool:
        return False
    def on_before_compile(self,code,magics)->Tuple[bool,str]:
        return False,''
    def on_after_compile(self,returncode,binfile,magics)->bool:
        return False
    def on_before_exec(self,code,magics)->Tuple[bool,str]:
        return False,''
    def on_after_exec(self,returncode,srcfile,magics)->bool:
        return False
    def on_after_completion(self,returncode,execfile,magics)->bool:
        return False
    def includehander(self,key, value,magics,line):
        # self.kobj._write_to_stdout(value+"\n")
        if len(value)>0:
            magics[key] = value
        else:
            magics[key] =''
            return ''
        if len(magics['include'])>0:
            index1=line.find('##%')
            # self.kobj._write_to_stdout("readcodefile\n")
            line=self.readcodefile(self,magics['include'],index1)
        return line
    def readcodefile(self,filename,spacecount=0):
        filecontent=''
        filecode=''
        codelist1=None
        if not os.path.exists(filename):
            return ''
        # self.kobj._log(os.path.join(os.path.abspath(''),filename+"\n"))
        with open(os.path.join(os.path.abspath(''),filename), 'r') as codef1:
            codelist1 = codef1.readlines()
        #扫描源码
        # filecode=codelist1
        if len(codelist1)>0:
            for t in codelist1:
                filecontent+=' '*spacecount + t
        try:
            newmagics,filecontent=self.kobj.mag.filter(filecontent)
        except Exception as e:
            self.kobj._log(str(e),3)
        return filecontent

import numpy as np
from OpenGL.GL import *


class Shader:
    def __init__(self, vertex_path, fragment_path):
        with open(vertex_path, 'r') as f:
            vertex_src = f.read()
        with open(fragment_path, 'r') as f:
            fragment_src = f.read()

        self.id = glCreateProgram()
        vs = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vs, vertex_src)
        glCompileShader(vs)
        
        # Check vertex shader compilation
        if not glGetShaderiv(vs, GL_COMPILE_STATUS):
            print("VERTEX SHADER COMPILE ERROR:")
            print(glGetShaderInfoLog(vs).decode())

        fs = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fs, fragment_src)
        glCompileShader(fs)
        
        # Check fragment shader compilation
        if not glGetShaderiv(fs, GL_COMPILE_STATUS):
            print("FRAGMENT SHADER COMPILE ERROR:")
            print(glGetShaderInfoLog(fs).decode())

        glAttachShader(self.id, vs)
        glAttachShader(self.id, fs)
        glLinkProgram(self.id)
        
        # Check program linking
        if not glGetProgramiv(self.id, GL_LINK_STATUS):
            print("PROGRAM LINK ERROR:")
            print(glGetProgramInfoLog(self.id).decode())
        else:
            print(f"Shader program {self.id} linked successfully")

        glDeleteShader(vs)
        glDeleteShader(fs)

    def use(self):
        glUseProgram(self.id)

    def set_mat4(self, name, mat):
        loc = glGetUniformLocation(self.id, name)
        glUniformMatrix4fv(loc, 1, GL_FALSE, mat.T.astype(np.float32))

    def set_vec2(self, name, vec):
        loc = glGetUniformLocation(self.id, name)
        glUniform2f(loc, *vec)

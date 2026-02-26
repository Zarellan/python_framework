from OpenGL.GL import *
from OpenGL.GL import shaders
import numpy as np
from Libraries.Windows import Windows

class PostProcessManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.fbo = None
        self.fbo_texture = None
        self.rbo = None  # optional depth/stencil
        self.postprocess_shader = None

        # Fullscreen quad setup
        self.quad_vao = glGenVertexArrays(1)
        self.quad_vbo = glGenBuffers(1)
        self._setup_fullscreen_quad()

        self.create_framebuffer(width, height)

    def _setup_fullscreen_quad(self):
        """Setup VAO/VBO for a fullscreen quad (NDC -1 to 1)"""
        quad_vertices = np.array([
            # positions   # texCoords
            -1.0, -1.0,   0.0, 0.0,
             1.0, -1.0,   1.0, 0.0,
            -1.0,  1.0,   0.0, 1.0,
             1.0,  1.0,   1.0, 1.0,
        ], dtype=np.float32)

        glBindVertexArray(self.quad_vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.quad_vbo)
        glBufferData(GL_ARRAY_BUFFER, quad_vertices.nbytes, quad_vertices, GL_STATIC_DRAW)

        # positions
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * quad_vertices.itemsize, ctypes.c_void_p(0))
        # texCoords
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * quad_vertices.itemsize, ctypes.c_void_p(2 * quad_vertices.itemsize))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def create_framebuffer(self, width, height):
        self.width = width
        self.height = height

        # Delete old FBO/texture if exist
        if hasattr(self, "fbo_texture") and self.fbo_texture:
            glDeleteTextures([self.fbo_texture])
        if hasattr(self, "fbo") and self.fbo:
            glDeleteFramebuffers(1, [self.fbo])
        if hasattr(self, "rbo") and self.rbo:
            glDeleteRenderbuffers(1, [self.rbo])

        # --- Texture ---
        self.fbo_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.fbo_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # --- Framebuffer ---
        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.fbo_texture, 0)

        # --- Optional depth/stencil renderbuffer ---
        self.rbo = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.rbo)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, self.rbo)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError("Framebuffer not complete!")

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def set_shader(self, shader_program):
        """Assign an OpenGL shader for post-processing"""
        self.postprocess_shader = shader_program

    def bind_fbo(self):
        """Call before rendering your scene"""
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glViewport(0, 0, self.width, self.height)
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def unbind_fbo(self):
        """Call to render to the screen instead of FBO"""
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, Windows.WIDTH, Windows.HEIGHT)

    def draw_fbo(self):
        """Draw the FBO fullscreen with shader applied"""
        glUseProgram(self.postprocess_shader or 0)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.fbo_texture)
        if self.postprocess_shader:
            loc = glGetUniformLocation(self.postprocess_shader, "screenTexture")
            glUniform1i(loc, 0)

        glBindVertexArray(self.quad_vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glBindVertexArray(0)

        glUseProgram(0)

    def resize(self, width, height):
        """Resize FBO when window size or virtual resolution changes"""
        self.create_framebuffer(width, height)

    def cleanup(self):
        """Delete OpenGL resources"""
        if self.fbo: glDeleteFramebuffers(1, [self.fbo])
        if self.fbo_texture: glDeleteTextures([self.fbo_texture])
        if self.rbo: glDeleteRenderbuffers(1, [self.rbo])
        if self.quad_vbo: glDeleteBuffers(1, [self.quad_vbo])
        if self.quad_vao: glDeleteVertexArrays(1, [self.quad_vao])
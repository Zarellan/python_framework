#version 330 core
in vec2 TexCoord;
out vec4 FragColor;

uniform sampler2D sprite_texture;
uniform float global_alpha;

void main() {
    vec4 texColor = texture(sprite_texture, TexCoord);
    FragColor = vec4(texColor.rgb, texColor.a * global_alpha);
}

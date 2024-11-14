#Wait for the video to open..

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import cv2
import threading
import os

def load_obj(filename):
    vertices = []
    faces = []
    
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return vertices, faces
    
    with open(filename) as file:
        for line in file:
            if line.startswith('v '):
                vertex = list(map(float, line.strip().split()[1:4]))
                vertices.append(vertex)
            elif line.startswith('f '):
                face = [int(part.split('/')[0]) - 1 for part in line.strip().split()[1:]]
                faces.append(face)
    return vertices, faces

def create_display_list(vertices, faces):
    display_list = glGenLists(1)
    glNewList(display_list, GL_COMPILE)
    
    glColor3f(0, 0, 1)  
    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()
    
    glColor3f(1, 1, 1)  
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    glEndList()
    return display_list

def display_obj_model(rotation_y_ref, rotation_x_ref):
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glClearColor(0, 0, 0, 1)

    vertices, faces = load_obj("vhs.obj")
    if not vertices or not faces:
        print("Error: OBJ file could not be loaded or is empty.")
        return

    display_list = create_display_list(vertices, faces)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        
        glRotatef(rotation_x_ref[0], 1, 0, 0)  
        glRotatef(rotation_y_ref[0], 0, 1, 0)  
        glCallList(display_list)
        
        glPopMatrix()
        pygame.display.flip()
        clock.tick(60)

def track_face_direction(rotation_y_ref, rotation_x_ref):
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    sensitivity_x = 20
    sensitivity_y = 15

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            face_center_x = x + w / 2
            face_center_y = y + h / 2
            
            if face_center_x < frame_width / 2 - sensitivity_x:
                rotation_y_ref[0] = max(rotation_y_ref[0] - 4, -30)
            elif face_center_x > frame_width / 2 + sensitivity_x:
                rotation_y_ref[0] = min(rotation_y_ref[0] + 4, 30)
            else:
                rotation_y_ref[0] = 0
            
            if face_center_y < frame_height / 2 - sensitivity_y:
                rotation_x_ref[0] = min(rotation_x_ref[0] + 4, 20)
            elif face_center_y > frame_height / 2 + sensitivity_y:
                rotation_x_ref[0] = max(rotation_x_ref[0] - 4, -20)
            else:
                rotation_x_ref[0] = 0

        cv2.imshow("Camera Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

rotation_y_ref = [0]
rotation_x_ref = [0]

if __name__ == "__main__":
    obj_thread = threading.Thread(target=display_obj_model, args=(rotation_y_ref, rotation_x_ref), daemon=True)
    cam_thread = threading.Thread(target=track_face_direction, args=(rotation_y_ref, rotation_x_ref), daemon=True)
    
    obj_thread.start()
    cam_thread.start()
    
    obj_thread.join()
    cam_thread.join()

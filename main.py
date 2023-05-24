import tkinter as tk
from PIL import ImageTk, Image
import apicalls
import pygame

target_height_per_image = 500
target_width = int(target_height_per_image * 0.9244060475161987)

class Robot:
    def __init__(self, on_image_path, off_image_path, name, voice="Adam"):
        self.name = name
        self.on_image = self.load_and_resize_image(on_image_path)
        self.off_image = self.load_and_resize_image(off_image_path)
        self.brain = apicalls.OpenAIBrain(self.name)
        self.clock = 0
        self.text = 'Salut'
        self.voice = voice
        self.voice_name = f"{self.name}_{self.clock}.mp3"
        self.is_talking = False

        # Generate script and audio during initialization
        self.get_script()
        self.generate_audio()

    def load_and_resize_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((target_width, target_height_per_image))
        return ImageTk.PhotoImage(image)

    def tick(self):
        self.clock += 1
        self.voice_name = f"{self.name}_{self.clock}.mp3"
        self.get_script()
        self.generate_audio()

    def get_image(self, is_activated):
        return self.on_image if is_activated else self.off_image
    def get_script(self):
        response = self.brain.call_API(self.clock, self.text)
        self.text = response
        return response  # return the generated response

    def generate_audio(self):
        apicalls.get_generate_audio(self.text, self.voice_name, voice=self.voice)
        # @TODO: check correct audio generation

    def set_talking(self, is_talking):
        self.is_talking = is_talking

    def play_audio(self):
        pygame.mixer.music.load(self.voice_name)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

class RobotApp:
    def __init__(self, root, robots):
        self.root = root
        self.robots = robots
        self.current_robot = 0
        self.image_labels = []
        self.root.bind('q', self.quit)
        self.conversation_history = []  # Initialize shared conversation history

        # Initialize Pygame's video system
        pygame.display.init()

    def quit(self, event):
        self.root.destroy()

    def update_robot_image(self, robot_index):
        robot = self.robots[robot_index]
        other_robot_index = (robot_index + 1) % len(self.robots)
        robot_image = robot.get_image(robot.is_talking)
        self.image_labels[robot_index].configure(image=robot_image)
        self.image_labels[robot_index].image = robot_image

    def animate_robot(self, robot_index):
        self.update_robot_image(robot_index)
        if self.robots[robot_index].is_talking:
            self.robots[robot_index].play_audio()

    def tick(self):
        for i, robot in enumerate(self.robots):
            # Perform tick operations on the current robot
            response = robot.tick()
            self.conversation_history.append(response)  # Add robot response to shared history

            # Update the image and play audio for the current robot
            self.update_robot_image(i)
            if robot.is_talking:
                self.animate_robot(i)

        # Update the conversation history of all robots before switching
        for robot in self.robots:
            robot.brain.update_content_data(' '.join(self.conversation_history[-10:]))

        self.root.after(200, self.switch_robot)

    def switch_robot(self):
        self.current_robot = (self.current_robot + 1) % len(self.robots)

        self.robots[self.current_robot].set_talking(True)
        self.robots[(self.current_robot + 1) % len(self.robots)].set_talking(False)

        for i, robot in enumerate(self.robots):
            self.update_robot_image(i)

        if self.robots[self.current_robot].is_talking:
            self.animate_robot(self.current_robot)

    def run(self):
        pygame.mixer.init()

        for i, robot in enumerate(self.robots):
            image_label = tk.Label(self.root)
            image_label.pack(side=tk.TOP)
            self.image_labels.append(image_label)

        self.switch_robot()

        # Check for Pygame events in the main event loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    print("Finished.")
                    self.robots[self.current_robot].is_talking = False
                    self.switch_robot()
                    # Call tick() method again after the audio has finished playing
                    self.robots[self.current_robot].tick()

            # Update Tkinter's event loop
            self.root.update_idletasks()
            self.root.update()

        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()

    robot1 = Robot('robot1-on.jpg', 'robot1-off.jpg', 'robot1', voice="Adam")
    robot2 = Robot('robot2-on.jpg', 'robot2-off.jpg','robot2', voice="Bella")

    robots = [robot1, robot2]

    app = RobotApp(root, robots)
    app.run()

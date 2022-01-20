'''WASD to move forwards, backwards,  and strafe left and right. left and right arrow to turn to the left and right. space to shoot, kill the boss in each room to win''' 



import random
from graphics3d import *
makeGraphicsWindow(800, 600)
def loadMap(world,myFile, dim):
    f=open(myFile,"r")
    coords=[]
    row= 0*dim
    for line in f:
        line=line.strip()
        column=1*dim
        row+=1*dim
        for char in line:
            if char == "X":
                coords.append(Wall(row, column))

            if char == "Q":
                world.mywalls2.append(Wall2(world,row, column))
            if char == "I":
                world.mywalls3.append(Wall3(world,row,column))
            if char =="S":
                setCameraPosition(row, 5, column)
            if char == "E":
                world.myenemies.append(Enemy(world, row,7,column))
            if char =="M":
                world.myenemies2.append(Enemy2(world,row,2,column))
            if char =="D":
                world.mydoors.append(Door(world,row,column))
            if char =="G":
                world.myfinalprizes.append(FinalPrize(world,row,0,column))
            if char == "R":
                world.boss2.append(Enemy2(world,row,5,column))
            if char == "Z":
                world.boss3.append(Enemy3(world, row , 7, column))
            
            
            
            column+=1*dim
    return coords
def inWall(currentx, currentz, boxx, boxz):
    return abs(currentx-boxx) < 6 and abs(currentz-boxz)<6
def inDoor(currentx, currentz, boxx, boxz):
    return abs(currentx-boxx) < 2.6 and abs(currentz-boxz)<2.6



class Wall:
    
    def __init__(self, x, z):
        self.x=x
        self.z=z
        self.wall=Box3D(3,40,3, texture= "ceiling.png")
    def draw(self):
        draw3D(self.wall, self.x, 0, self.z)
class Door:
    def __init__(self,world,x,z):
        self.x=x
        self.z=z
        self.door=Box3D(3,40,3, texture = "Golden_snakeskin_pxr128.png")
    def draw(self):
        draw3D(self.door,self.x, 0, self.z)

class Wall2:
    def __init__(self,world, x, z):
        self.x=x
        self.z=z
        self.wall=Box3D(8,40,8, texture= "clownwall.png")
    def start(self,world):
        self.wall=Box3D(8,40,4, texture = "clownwall.png")
    def update(self,world):
        pass
    def draw(self,world):
        draw3D(self.wall, self.x, 0, self.z)

class Wall3:
    def __init__(self,world, x, z):
        self.x=x
        self.z=z
        self.wall=Box3D(5,40,5,texture= "wall.png")
    def start(self,world):
        self.wall=Box3D(5,40,5,texture="wall.png")
    def update(self,world):
        pass
    def draw(self,world):
        draw3D(self.wall, self.x, 0, self.z)

class Vector:
    def __init__(self,  somex, somey, somez):
        self.somex= somex
        self.somey= somey
        self.somez= somez
        
        



class Smallenemy:
    def __init__(self,world,x,y,z):
        self.x=x
        self.y=y
        self.z=z
        self.velocity=Vector(0,0,0)
        self.fireball= Fireball(world,self.x,self.y,self.z)
        self.thing= Sphere3D(2, texture= "face.png")
        self.health=3
        self.rotatey=0
    def start(self, world):
        self.thing= Sphere3D(2, texture= "face.png")

    def update(self, world):
        (cameraX, cameraY, cameraZ) = getCameraPosition()
        distance=((cameraX-self.x)**2+(cameraY-self.y)**2+(cameraZ-self.z)**2)**0.5
        if distance < 5 and world.immune==False and world.health > 0:
            world.health-=10
            world.immune=True
            world.pain = True
        if world.immune== True:
            world.invincibilityframes+=1
        if world.invincibilityframes == 200:
            world.immune=False
            world.invincibilityframes=0
            
        self.fireball.update(world)
        
        if world.firerate % 80 == 0:
            self.fireball= Fireball(world, self.x, self.y, self.z)
            (tempX, tempY, tempZ) = getCameraPosition()  
            self.fireball.velocity=Vector(self.fireball.x-tempX, self.fireball.y-tempY, self.fireball.z-tempZ)
        self.fireball.x-=0.05*self.fireball.velocity.somex
        self.fireball.y-= 0.05*self.fireball.velocity.somey
        self.fireball.z-=0.05*self.fireball.velocity.somez  
        self.velocity=Vector(self.x-cameraX, self.y-cameraY, self.z-cameraZ)
        self.rotatey=cartesianToPolarAngle(self.velocity.somex,self.velocity.somez)+90
        self.x-=0.02*self.velocity.somex
        self.y-= 0.02*self.velocity.somey
        self.z-=0.02*self.velocity.somez
        for bullet in world.mybullets:
            distance=((bullet.x-self.x)**2+(bullet.y-self.y)**2+(bullet.z-self.z)**2)**0.5
            if distance < 2:
                self.health-=1
                world.mybullets.remove(bullet)
            if self.health == 0:
                world.myenemiesmall.remove(self)
                return
                        
                
    
    def draw(self, world):
        draw3D(self.thing, self.x, self.y, self.z,0,self.rotatey)
        self.fireball.draw(world)    

class Fireball:
    def __init__(self, world,x,y,z):
        self.x= x
        self.y=y
        self.z=z
        self.velocity=Vector(0,0,0)
        self.thing= Sphere3D(2,texture= "fireball.png")
    
    def update(self, world):
        
        (cameraX, cameraY, cameraZ) = getCameraPosition()
        distance=((cameraX-self.x)**2+(cameraY-self.y)**2+(cameraZ-self.z)**2)**0.5
        if distance < 5 and world.immune==False and world.health > 0:
            world.health-=10
            world.immune=True
            world.pain= True
        if world.immune== True:
            world.invincibilityframes+=1
        if world.invincibilityframes == 200:
            world.immune=False
            world.invincibilityframes=0
        
    def draw(self, world):
        draw3D(self.thing, self.x, self.y, self.z)

class Fireball2:
    def __init__(self, world,x,y,z):
        self.x= x
        self.y=y
        self.z=z
        self.velocity=Vector(0,0,0)
        self.thing= Sphere3D(2,texture= "lightning.png")
    
    def update(self, world):
        
        (cameraX, cameraY, cameraZ) = getCameraPosition()
        distance=((cameraX-self.x)**2+(cameraY-self.y)**2+(cameraZ-self.z)**2)**0.5
        if distance < 5 and world.immune==False and world.health > 0:
            world.health-=10
            world.immune=True
            world.pain = True
        if world.immune== True:
            world.invincibilityframes+=1
        if world.invincibilityframes == 200:
            world.immune=False
            world.invincibilityframes=0
        
    def draw(self, world):
        draw3D(self.thing, self.x, self.y, self.z)



class Explosive:
    def __init__(self, world, x, y, z):
        self.x=x
        self.y=y
        self.z=z
        self.velocity=Vector(0,0,0)
        self.thing=Sphere3D(2, texture= "missile.png")
        self.counter=0
        self.health=3
    def update(self, world):
        self.counter+=1
        for bullet in world.mybullets:
            distance=((bullet.x-self.x)**2+(bullet.y-self.y)**2+(bullet.z-self.z)**2)**0.5
            if distance < 2:
                self.health-=1
                world.mybullets.remove(bullet)
            if self.health == 0:
                world.mymissiles.remove(self)
                return        
        
        (cameraX, cameraY, cameraZ) = getCameraPosition()
        distance=((cameraX-self.x)**2+(cameraY-self.y)**2+(cameraZ-self.z)**2)**0.5
        if distance < 2 and world.immune==False and world.health > 0:
            world.health-=10
            world.immune=True
            world.pain = True
            world.mymissiles.remove(self)
            return
        if world.immune== True:
            world.invincibilityframes+=1
        if world.invincibilityframes == 200:
            world.immune=False
            world.invincibilityframes=0
        
        if world.missilecounter%40==0:
            self.velocity=Vector(self.x-cameraX, self.y-cameraY, self.z-cameraZ)
        if self.counter < 30:
            self.x-=0.02*self.velocity.somex
            self.y-= 0.02*self.velocity.somey
            self.z-=0.02*self.velocity.somez  
    def draw(self, world):
        draw3D(self.thing, self.x, self.y, self.z)
                
     
        
        
    

class Weakspot:
    def __init__(self, world, x, y, z):
        self.x= x
        self.y= y
        self.z= z
        self.thing = Sphere3D(3, texture= "clown.png")
        self.velocity = Vector(0,0,0)
        self.rotatey=0
    def start(self, world):
        self.rotatey=0
        
        self.thing = Sphere3D(3, texture= "clown.png")
    def update(self,world):
        if world.missilecounter % 40 ==0:
            world.mymissiles.append(Explosive(world, self.x, self.y, self.z))
        (cameraX, cameraY, cameraZ) = getCameraPosition()
        self.velocity=Vector(self.x-cameraX, self.y-cameraY, self.z-cameraZ) 
        self.rotatey=cartesianToPolarAngle(self.velocity.somex,self.velocity.somez)+90
        
            
    def draw(self, world):
        draw3D(self.thing, self.x, self.y, self.z,0,self.rotatey)
        
class Boomerang:
    def __init__(self, world, x, y, z):
        self.x=x
        self.y=y
        self.z=z
        self.velocity= Vector(0,0,0)
        self.thing =Torus3D(2, 0.7 ,texture = "boomerang.png")
    def start(self, world):
        self.thing =Torus3D(2, 0.7,texture = "boomerang.png")
    def update(self, world):
        (cameraX, cameraY, cameraZ) = getCameraPosition()
        distance=((cameraX-self.x)**2+(cameraY-self.y)**2+(cameraZ-self.z)**2)**0.5
        if distance < 2 and world.immune==False and world.health > 0:
            world.health-=10
            world.immune=True
            world.pain = True
        if world.immune== True:
            world.invincibilityframes+=1
        if world.invincibilityframes == 200:
            world.immune=False
            world.invincibilityframes=0
    def draw(self, world):
        draw3D(self.thing, self.x, self.y, self.z)
        
class Thunder:
    def __init__(self, world, x, y, z, velx, vely, velz):
        self.x=x
        self.y=y
        self.z=z
        self.velx = velx
        self.vely= vely
        self.velz = velz        
        self.thing = Torus3D(4, 0.5, texture = "thunder.png")
    def start(self, world):
        self.thing = Torus3D(4, 0.5, texture = "thunder.png")
    def update(self, world):
        (cameraX, cameraY, cameraZ) = getCameraPosition()
        distance=((cameraX-self.x)**2+(cameraY-self.y)**2+(cameraZ-self.z)**2)**0.5
        if distance < 4 and world.immune==False and world.health > 0:
            world.health-=10
            world.immune=True
            world.pain = True
        if world.immune== True:
            world.invincibilityframes+=1
        if world.invincibilityframes == 200:
            world.immune=False
            world.invincibilityframes=0   
        self.x += 0.35*self.velx
        self.y +=0.35*self.vely
        self.z+= 0.35*self.velz
        for wall in world.coords:
            if inWall(self.x, self.z, wall.x, wall.z):
                world.thunder.remove(self)
                return 
        for door in world.mydoors:
            if inDoor(self.x, self.z, wall.x, wall.z):
                world.thunder.remove(self)
                return
    
    def draw(self, world):
        draw3D(self.thing, self.x, self.y, self.z)
    
    
             
class Enemy:
    def __init__(self,world,x,y,z):
        self.x=x
        self.y=y
        self.z=z
       
        self.velocity=Vector(0,0,0)
        self.fireball= Fireball(world,self.x,self.y,self.z)
        self.fireball2= Fireball(world,self.x,self.y, self.z)
        self.fireball3= Fireball(world,self.x,self.y, self.z)
        self.rotatey=0
        
    def start(self, world):
        self.thing2= Sphere3D(7, texture= "skulls.png")

    def update(self, world):
        if world.boss1alive ==True:
            (cameraX, cameraY, cameraZ) = getCameraPosition()
            distance=((cameraX-self.x)**2+(cameraY-self.y)**2+(cameraZ-self.z)**2)**0.5
            if distance < 5 and world.immune==False and world.health > 0:
                world.health-=10
                world.immune=True
                world.pain = True
                
                
            if world.immune== True:
                world.invincibilityframes+=1
            if world.invincibilityframes == 200:
                world.immune=False
                world.invincibilityframes=0
                
            self.fireball.update(world)
            self.fireball2.update(world)
            self.fireball3.update(world)
     
            if world.firerate % 90 == 0:
                self.fireball= Fireball(world, self.x, self.y, self.z)
                (tempX, tempY, tempZ) = getCameraPosition()
        
                self.fireball.velocity=Vector(self.fireball.x-tempX, self.fireball.y-tempY, self.fireball.z-tempZ)
            self.fireball.x-=0.07*self.fireball.velocity.somex
            self.fireball.y-= 0.07*self.fireball.velocity.somey
            self.fireball.z-=0.07*self.fireball.velocity.somez             
           
            if world.firerate2 % 90 == 0:
                self.fireball2= Fireball(world, self.x, self.y, self.z)
                (tempX, tempY, tempZ) = getCameraPosition()
            
                self.fireball2.velocity=Vector(self.fireball2.x-tempX, self.fireball2.y-tempY, self.fireball2.z-tempZ)
            self.fireball2.x-=0.07*self.fireball2.velocity.somex
            self.fireball2.y-= 0.07*self.fireball2.velocity.somey
            self.fireball2.z-=0.07*self.fireball2.velocity.somez          
            
     
            if world.firerate3 % 90 == 0:
                self.fireball3= Fireball(world, self.x, self.y, self.z)
                (tempX, tempY, tempZ) = getCameraPosition()
            
                self.fireball3.velocity=Vector(self.fireball3.x-tempX, self.fireball3.y-tempY, self.fireball3.z-tempZ)
            self.fireball3.x-=0.07*self.fireball3.velocity.somex
            self.fireball3.y-= 0.07*self.fireball3.velocity.somey
            self.fireball3.z-=0.07*self.fireball3.velocity.somez                               
            
            
            self.velocity=Vector(self.x-cameraX, self.y-cameraY, self.z-cameraZ)
            self.rotatey=cartesianToPolarAngle(self.velocity.somex,self.velocity.somez)+90
            self.x-=0.003*self.velocity.somex
            self.z-=0.003*self.velocity.somez
                        
            
                    
                 
    
    def draw(self, world):
        draw3D(self.thing2, self.x, self.y, self.z,0,self.rotatey)
        self.fireball.draw(world)
        self.fireball2.draw(world)
        self.fireball3.draw(world)
    
class Enemy2:
    def __init__(self,world,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def start(self, world):
        
        self.thing3= Sphere3D(3, texture= "clown2.png")
        self.weakspot = Weakspot(world, self.x, self.y, self.z)
        self.aggro = False
        self.waittime=0
        self.distance=0
        self.boomerang= Boomerang(world, self.x, self.z , self.y)
        self.boomerang2=Boomerang(world, self.x, self.z, self. y)
        self.rebound=False
        self.reboundcounter=0
        self.rebound2=False
        self.reboundcounter2=0  
        self.aggro2 = False

        self.rotatey=0
        


        
        
    def update(self, world):
        (oldx, cameraY, cameraZ) = getCameraPosition()
        (cameraX, cameraY, cameraZ) = getCameraPosition()
        self.distance=((cameraX-self.x)**2+(cameraY-self.y)**2+(cameraZ-self.z)**2)**0.5
        if world.boss1alive == False and self.distance< 70:
            world.boss2alive = True
        
            
        if self.distance <70:
            world.boss2alive = True
            world.bosscounter2 =1
        if world.boss2alive == True:
            self.weakspot.update(world)

            
            if world.boomerangfire % 60 == 0:
                self.reboundcounter=0
                self.boomerang= Boomerang(world, self.x, self.y, self.z)
                (tempX, tempY, tempZ) = getCameraPosition()
                self.rebound=False
                self.boomerang.velocity=Vector(self.boomerang.x-tempX, self.boomerang.y-tempY, self.boomerang.z-tempZ)
            if self.rebound == False:
                self.boomerang.x-=0.05*self.boomerang.velocity.somex
                self.boomerang.y-= 0.05*self.boomerang.velocity.somey
                self.boomerang.z-=0.05*self.boomerang.velocity.somez  
                self.reboundcounter+=1
            if self.reboundcounter ==30:
                self.rebound=True  
                    
            if self.rebound == True:
                self.boomerang.x+=0.05*self.boomerang.velocity.somex
                self.boomerang.y+= 0.05*self.boomerang.velocity.somey
                self.boomerang.z+=0.05*self.boomerang.velocity.somez
            
                
            for wall in world.coords:
                if inWall(self.boomerang.x, self.boomerang.z, wall.x, wall.z):
                    self.rebound = True
                    
            
            self.boomerang.update(world)
            
            if world.boomerangfire2 % 60 == 0:
                self.rebouncounter=0
                self.boomerang2= Boomerang(world, self.x, self.y, self.z)
                (tempX, tempY, tempZ) = getCameraPosition()
                self.rebound2=False
                self.boomerang2.velocity=Vector(self.boomerang2.x-tempX, self.boomerang2.y-tempY, self.boomerang2.z-tempZ)
            if self.rebound2 == False:
                self.boomerang2.x-=0.05*self.boomerang2.velocity.somex
                self.boomerang2.y-= 0.05*self.boomerang2.velocity.somey
                self.boomerang2.z-=0.05*self.boomerang2.velocity.somez  
                self.reboundcounter2+=1
            if self.reboundcounter2 ==30:
                self.rebound2=True  
                    
            if self.rebound2 == True:
                self.boomerang2.x+=0.05*self.boomerang2.velocity.somex
                self.boomerang2.y+= 0.05*self.boomerang2.velocity.somey
                self.boomerang2.z+=0.05*self.boomerang2.velocity.somez
            
                
            for wall in world.mywalls2:
                if inWall(self.boomerang2.x, self.boomerang2.z, wall.x, wall.z):
                    self.rebound2 = True
            
            for door in world.coords:
                if inDoor(self.boomerang2.x, self.boomerang2.z, door.x, door.z):
                    self.rebound2 = True
                    
                    
            (self.oldx, self.oldy, self.oldz)=(self.x,self.y,self.z)
            (self.oldx2, self.oldy2, self.oldz2)=(self.weakspot.x,self.weakspot.y,self.weakspot.z)
            (cameraX, cameraY, cameraZ) = getCameraPosition()
            self.weakspot.velocity=Vector(self.weakspot.x-cameraX, self.weakspot.y-cameraY, self.weakspot.z-cameraZ)
            if self.aggro==False:
                self.weakspot.x+=self.weakspot.velocity.somex *0.01
                self.weakspot.z+=self.weakspot.velocity.somez *0.01 
            if self.aggro == True:
                self.weakspot.x-=self.weakspot.velocity.somex *0.01
                self.weakspot.z-=self.weakspot.velocity.somez *0.01                 
                
            for wall in world.coords:
                if inWall(self.weakspot.x, self.weakspot.z, wall.x ,wall.z):
                    self.weakspot.x=self.oldx2
                    self.weakspot.y=self.oldy2
                    self.weakspot.z=self.oldz2
                    self.aggro = True
            for wall in world.mywalls2:
                if inWall(self.weakspot.x, self.weakspot.z, wall.x ,wall.z):
                    self.weakspot.x=self.oldx2
                    self.weakspot.y=self.oldy2
                    self.weakspot.z=self.oldz2
                    self.aggro = True
                    
            if world.aggrocounter %100==0:
                self.aggro=False

                
                    
            for door in world.mydoors:
                if inDoor(self.weakspot.x,self.weakspot.z, door.x, door.z):
                    self.weakspot.x=self.oldx2
                    self.weakspot.y=self.oldy2
                    self.weakspot.z=self.oldz2
                    self.aggro= True
                               
                                       
            distance=((cameraX-self.x)**2+(cameraY-self.y)**2+(cameraZ-self.z)**2)**0.5
            if distance < 5 and world.immune==False and world.health > 0:
                world.health-=10
                world.immune=True
                world.pain = True
            if world.immune== True:
                world.invincibilityframes+=1
            if world.invincibilityframes == 200:
                world.immune=False
                world.invincibilityframes=0
            
            (self.oldx, self.oldy, self.oldz)=(self.x,self.y,self.z)
    
            (zoomX, zoomY, zoomZ)= getCameraPosition()  
            self.velocity=Vector(self.x-zoomX, self.y-zoomY, self.z- zoomZ)
            self.rotatey=cartesianToPolarAngle(self.velocity.somex,self.velocity.somez)+90
            if self.aggro2== True:
                self.x-=0.015*self.velocity.somex
                self.z-=0.015*self.velocity.somez  
            if self.aggro2== False:
                self.x+=0.015*self.velocity.somex
                self.z+=0.015*self.velocity.somez                  
            
            if world.aggrocounter2 %100==0:
                self.aggro2=False
                
                
            for wall in world.coords:
                if inWall(self.x, self.z, wall.x ,wall.z):
                    self.x=self.oldx
                    self.y=self.oldy
                    self.z=self.oldz
                    self.aggro2= True
            for wall in world.mywalls2:
                if inWall(self.x, self.z, wall.x ,wall.z):
                    self.x=self.oldx
                    self.y=self.oldy
                    self.z=self.oldz
                    self.aggro2= True
                   
                   
                    
            for door in world.mydoors:
                if inDoor(self.x,self.z, door.x, door.z):
                    self.x=self.oldx
                    self.y=self.oldy
                    self.z=self.oldz
                    self.aggro2= True         
                       
    def draw(self, world):
        draw3D(self.thing3, self.x, self.y, self.z, 0, self.rotatey)  
        self.weakspot.draw(world)
        self.boomerang.draw(world)
        
class Enemy3:
    def __init__(self, world, x, y, z):
        self.x=x
        self.y=y
        self.z=z
        self.thing= Sphere3D(6, texture ="eye.png")
        self.fireball= Fireball2(world,self.x,self.y,self.z)
        self.firing=0
        self.fireball2= Fireball2(world,self.x,self.y, self.z)
        self.fireball3= Fireball2(world,self.x,self.y, self.z)   
        self.fireball4= Fireball2(world,self.x,self.y, self.z)
        self.fireball5= Fireball2(world,self.x,self.y, self.z)   
        self.rotatey=0
        self.lasercounter=0
        self.laserfire=0
        self.somevelocity= Vector(0,0,0)
        self.rings =0
        self.ringbool = False
    def start(self,world):
        self.thing= Sphere3D(6.5, texture ="eye.png")
        self.distance=0
        self.firing=0
        self.lasercounter=0
        self.somevelocity= Vector(0,0,0)
        self.rings = 0
        self.ringbool = False
    def update(self,world):
        
        (cameraX, cameraY, cameraZ) = getCameraPosition()
        self.distance=((cameraX-self.x)**2+(cameraY-self.y)**2+(cameraZ-self.z)**2)**0.5
        
        if world.boss2alive == False and self.distance< 40:
            world.boss3alive = True
        
        if world.boss3alive ==True:
            self.firing+=1
            self.rings+=1
            self.laserfire+=1
            world.bosscounter3=1
            (cameraX, cameraY, cameraZ) = getCameraPosition()
            distance=((cameraX-self.x)**2+(cameraY-self.y)**2+(cameraZ-self.z)**2)**0.5
            if distance < 5 and world.immune==False and world.health > 0:
                world.health-=10
                world.immune=True
                world.pain = True
            if world.immune== True:
                world.invincibilityframes+=1
            if world.invincibilityframes == 200:
                world.immune=False
                world.invincibilityframes=0
            
                
            self.fireball.update(world)
            self.fireball2.update(world)
            self.fireball3.update(world)
            self.fireball4.update(world)
            self.fireball5.update(world)
     
            if self.firing% 60 == 0:
                self.fireball= Fireball2(world, self.x, self.y, self.z)
                self.fireball2= Fireball2(world, self.x, self.y, self.z)
                self.fireball3= Fireball2(world, self.x, self.y, self.z)
                self.fireball4= Fireball2(world, self.x, self.y, self.z)
                self.fireball5= Fireball2(world, self.x, self.y, self.z)
                (tempX, tempY, tempZ) = getCameraPosition()
                self.fireball.velocity=Vector(self.fireball.x-tempX+random.randint(-4, 4), self.fireball.y-tempY+random.randint(-4, 4), self.fireball.z-tempZ+random.randint(-4, 4))
                self.fireball2.velocity=Vector(self.fireball2.x-tempX+random.randint(-4, 4), self.fireball2.y-tempY+random.randint(-4, 4), self.fireball2.z-tempZ+random.randint(-4, 4))
                self.fireball3.velocity=Vector(self.fireball3.x-tempX+random.randint(-4, 4), self.fireball3.y-tempY+random.randint(-4, 4), self.fireball3.z-tempZ+random.randint(-4, 4))
                self.fireball4.velocity=Vector(self.fireball4.x-tempX+random.randint(-4, 4), self.fireball4.y-tempY+random.randint(-4, 4), self.fireball4.z-tempZ+random.randint(-4, 4))
                self.fireball5.velocity=Vector(self.fireball5.x-tempX+random.randint(-4, 4), self.fireball5.y-tempY+random.randint(-4, 4), self.fireball5.z-tempZ+random.randint(-4, 4))
            
            self.fireball.x-=0.07*self.fireball.velocity.somex
            self.fireball.y-= 0.07*self.fireball.velocity.somey
            self.fireball.z-=0.07*self.fireball.velocity.somez             
            self.fireball2.x-=0.07*self.fireball2.velocity.somex
            self.fireball2.y-= 0.07*self.fireball2.velocity.somey
            self.fireball2.z-=0.07*self.fireball2.velocity.somez          
            self.fireball3.x-=0.07*self.fireball3.velocity.somex
            self.fireball3.y-= 0.07*self.fireball3.velocity.somey
            self.fireball3.z-=0.07*self.fireball3.velocity.somez  
            self.fireball4.x-=0.07*self.fireball4.velocity.somex
            self.fireball4.y-= 0.07*self.fireball4.velocity.somey
            self.fireball4.z-=0.07*self.fireball4.velocity.somez          
            self.fireball5.x-=0.07*self.fireball5.velocity.somex
            self.fireball5.y-= 0.07*self.fireball5.velocity.somey
            self.fireball5.z-=0.07*self.fireball5.velocity.somez                  

            self.velocity=Vector(self.x-cameraX, self.y-cameraY, self.z-cameraZ)
            self.rotatey=cartesianToPolarAngle(self.velocity.somex,self.velocity.somez)+90
            self.x-=0.009*self.velocity.somex
            self.z-=0.009*self.velocity.somez
            if self.rings % 80 ==0:
                self.ringbool = True
            else:
                self.ringbool= False
            
            if self.ringbool == True:
                world.thunder.append(Thunder(world,self.x, 5,self.z, 10, 0,0))
                world.thunder.append(Thunder(world,self.x, 5,self.z, 0, 0,-10))
                world.thunder.append(Thunder(world,self.x, 5,self.z, -10, 0,0))
                world.thunder.append(Thunder(world,self.x, 5,self.z, 10, 0,-10))
                world.thunder.append(Thunder(world,self.x, 5,self.z, 10, 0,10))
                world.thunder.append(Thunder(world,self.x, 5,self.z, 10, 0,-10))
                world.thunder.append(Thunder(world,self.x, 5,self.z, 0, 0,10))
                world.thunder.append(Thunder(world,self.x, 5,self.z, 0, 0,-10))
                                                          
                
                
                
            if self.laserfire %  120 ==0:
                self.lasercounter+=1
                (camX, camY, camZ) = getCameraPosition()
                self.somevelocity= Vector(camX- self.x, camY-self.y, camZ-self.z)
            
            if self.lasercounter > 30:
                self.lasercounter=0
            if self.lasercounter >0:
                world.mylasers.append(Laser(world, self.x, self.y, self.z, self.somevelocity.somex, self.somevelocity.somey, self.somevelocity.somez))

        
    def draw(self, world):
        draw3D(self.thing,self.x, self.y, self.z, 0, self.rotatey)
        self.fireball.draw(world)
        self.fireball2.draw(world)
        self.fireball3.draw(world)
        self.fireball4.draw(world)
        self.fireball5.draw(world)   
        
        
        

class Projectile:
    def __init__ (self, world, x, y, z,vectorx,vectory,vectorz):
        self.x=x
        self.y=y
        self.z=z
        self.vectorx=vectorx
        self.vectory=vectory
        self.vectorz=vectorz
        
        self.thing3= Sphere3D(0.25,texture = "bullet.png")
    def start(self,world):
        self.thing3= Sphere3D(0.5,texture = "bullet.png")
        
        
    def update(self,world):
        for wall in world.coords:
            if inWall(self.x, self.z, wall.x ,wall.z):
                world.mybullets.remove(self) 
                return
        for wall in world.mywalls2:
            if inWall(self.x, self.z, wall.x ,wall.z):
                world.mybullets.remove(self) 
                return
                        
        for boss in world.myenemies:
            distance=((boss.x-self.x)**2+(boss.y-self.y)**2+(boss.z-self.z)**2)**0.5
            if distance < 7 and world.shotgun == True:
                world.bosshealth -=0.8
                world.mybullets.remove(self) 
                return
            if distance < 7 and world.rifle == True:
                world.bosshealth -=1.1
                world.mybullets.remove(self) 
                return            
        
        for boss in world.boss2:
            distance=((boss.x-self.x)**2+(boss.y-self.y)**2+(boss.z-self.z)**2)**0.5
            if distance < 4 and world.boss2alive==True and world.shotgun == True:
                world.bosshealth2 -=0.8
                world.mybullets.remove(self) 
                return
            if distance < 4 and world.rifle == True:
                world.bosshealth2 -=1.1
                world.mybullets.remove(self) 
                return                        
        
        for boss in world.boss2:
            distance =((boss.weakspot.x-self.x)**2+(boss.weakspot.y-self.y)**2+(boss.weakspot.z-self.z)**2)**0.5
            if distance < 4 and world.boss2alive==True and world.shotgun == True:
                world.bosshealth2 -=0.8
                world.mybullets.remove(self)  
            if distance < 4 and world.rifle == True:
                world.bosshealth2 -=1.1
                world.mybullets.remove(self) 
                return        
        for boss in world.boss3:
            distance =((boss.x-self.x)**2+(boss.y-self.y)**2+(boss.z-self.z)**2)**0.5
            if distance < 7 and world.boss3alive==True and world.shotgun == True:
                world.bosshealth3 -=0.8
                world.mybullets.remove(self)  
            if distance < 7 and world.rifle == True:
                world.bosshealth3 -=1.1
                world.mybullets.remove(self) 
                return        
       
        self.x+=6*self.vectorx
        self.y+=6*self.vectory
        self.z+=6*self.vectorz
        
        #for door in world.mydoors:
            #if inDoor(self.x, self.z, door.x ,door.z):
                #world.mybullets.remove(self) 
                #return
        
    def draw(self,world):
        draw3D(self.thing3, self.x, self.y, self.z)
        
        
        
        
class Laser:
    def __init__(self, world,x,y,z, velx, vely, velz):
        self.x= x
        self.y=y
        self.z=z
        self.velocity=Vector(0,0,0)
        self.thing= Sphere3D(2,texture= "plasma.png")
        self.velx=velx
        self.vely=vely
        self.velz=velz
    
    def update(self, world):
        
        (cameraX, cameraY, cameraZ) = getCameraPosition()
        distance=((cameraX-self.x)**2+(cameraY-self.y)**2+(cameraZ-self.z)**2)**0.5
        if distance < 5 and world.immune==False and world.health > 0:
            world.health-=10
            world.immune=True
            world.pain = True
        if world.immune== True:
            world.invincibilityframes+=1
        if world.invincibilityframes == 200:
            world.immune=False
            world.invincibilityframes=0

        self.x+=0.1*self.velx
        self.y+=0.1*self.vely
        self.z+=0.1*self.velz
        
        
        for wall in world.coords:
            if inWall(self.x, self.z, wall.x, wall.z):
                world.mylasers.remove(self)
                return 
        for door in world.mydoors:
            if inDoor(self.x, self.z, wall.x, wall.z):
                world.mylasers.remove(self)
                return
    
    
        
        
    def draw(self, world):
        draw3D(self.thing, self.x, self.y, self.z)    
        
                    
                 

class FinalPrize:
    def __init__(self, world, x, y, z):
        self.x=x
        self.y=y
        self.z=z
    def start(self, world):
        self.thing3= Box3D(3,3,3, texture= "gems.png") 
    def update(self, world):
        (cameraX, cameraY, cameraZ) = getCameraPosition()
        distance=((cameraX-self.x)**2+(cameraY-self.y)**2+(cameraZ-self.z)**2)**0.5
        if distance < 5:
            world.points+=1
            world.win=True
    def draw(self, world):
        draw3D(self.thing3, self.x,self.y,self.z)
            
        
        
    
    
     
    

def startWorld(world):
    world.boomerangreturn=False
    world.blood= loadImage("blood.png")
    world.assault= loadImage("assaultrifle.png")
    world.shotgun3 = loadImage("shotgunpicture.png")
    world.shotgunimage = loadImage("shotgun.png")
    world.shotgunimage2 = loadImage ("shotgun2.png")
    world.gunfire = loadImage("2.png")
    world.gunfire2 = loadImage("1.png")
    world.gunfire3=loadImage("3.png")
    world.crosshair = loadImage("crosshair.png")
    world.ammoimage=loadImage("ammo.png")
    world.doom=loadImage("doom.png")
    world.mycanvas= Canvas2D(800, 600,1.0)
    world.othercanvas= Canvas2D(800, 600,0.4)
    world.mydoors= []
    world.x_axis = Lines3D([(-50,0,0), (50,0,0)], "red", 4) 
    world.origin = Torus3D(5, 1)
    world.y_axis =Lines3D([(0,-50,0), (0,50,0)], "yellow", 4)
    world.z_axis =Lines3D([(0,-0,-50), (0,0,50)], "blue", 4)
    world.shape1 = Torus3D(5, 1)
    world.shape2 = Torus3D(5, 1)
    world.shape3 = Torus3D(5, 1)
    world.ceiling = Rect3D( 650, 650, texture = "something.png")
    world.floor= Rect3D(650, 650, texture = "something.png")
    world.time=0
    world.ammo=30
    world.immune=False
    world.firerate = 0
    world.isfire= False
    world.fire=False
    world.win=False
    world.bosshealth= 100
    world.distance=0
    world.myfirerate=0
    world.myprizes=[]
    world.myenemies=[]
    world.myenemies2=[]
    world.myenemiesmall=[]
    world.myfinalprizes=[]
    world.mybullets=[]
    world.boss2=[]
    world.mymissiles=[]
    world.mywalls2=[]
    world.mywalls3=[]
    world.thunder= []
    world.boomerangfire=0
    world.boomerangfire2=30
    world.boss3=[]
    world.bosscounter3=0
    world.mylasers=[]


    world.charging=False
    world.spawn=0
    world.coords=loadMap(world,"textfile.txt", 3)
    for prize in world.myprizes:
        prize.start(world)
    world.health=100
    world.invincibilityframes=0
    world.firerate2= 30
    world.firerate3= 60
    world.firing=0
    world.boss1alive = True
    world.bosscounter = 1
    world.rotation=0
    world.boss2alive = False
    world.boss2distance=0
    world.bosshealth2=100
    world.bosshealth3=100
    world.aggrocounter=0
    world.firing=False
    world.animate=0
    world.count=0
    world.missilecounter=0
    world.ammoload=0
    world.bosscounter2=0
    world.boomerangreturn2=False
    world.aggrocounter2=0
    world.boss3alive=False
    world.pain= False
    world.paincounter =0
    world.startscreen = True
    world.rifle = False
    world.shotgun = False
    world.rockets = False

    
    
    
    for enemy in world.myenemies:
        enemy.start(world)
    for enemy in world.myenemies2:
        enemy.start(world)
    for enemy in world.myenemiesmall:
        enemy.start(world)
    for prize in world.myfinalprizes:
        prize.start(world) 
    for bullet in world.mybullets:
        bullet.start(world)
    for boss in world.boss2:
        boss.start(world)
    for missile in world.mymissiles:
        missile.start(world)
    for boss in world.boss3:
        boss.start(world)
    for laser in world.mylasers:
        laser.start(world)
    for wall in world.mywalls2:
        wall.start(world)
    for wall in world.mywalls3:
        wall.start(world) 
    for thing in world.thunder:
        thing.start(world)
    
    world.points=0
    if world.boss2alive==True:
        world.bosscounter2=1

        world.missilecounter+=1
    

    
    
    
def shoot(world):
    if world.health>0 and world.ammo>0 and world.rifle == True:
        world.count+=1
        world.ammo-=1
        world.firing=True
        print world.ammo
        (cameraX, cameraY, cameraZ) = getCameraPosition()
        (cameraHeading, cameraPitch, cameraRoll) = getCameraRotation()
        (world.shootx,world.shooty,world.shootz)=sphericalToCartesian(cameraHeading,cameraPitch,0.5)
        
       
        for i in range(1):
            world.mybullets.append(Projectile(world,cameraX,cameraY,cameraZ,world.shootx, world.shooty, world.shootz))
    
    if world.health>0 and world.ammo>0 and world.shotgun == True:
        world.count+=1
        world.ammo-=1
        world.firing=True
        print world.ammo
        (cameraX, cameraY, cameraZ) = getCameraPosition()
        (cameraHeading, cameraPitch, cameraRoll) = getCameraRotation()
        (world.shootx,world.shooty,world.shootz)=sphericalToCartesian(cameraHeading,cameraPitch,0.5)
        
        
        for i in range(5):
            world.mybullets.append(Projectile(world,cameraX,cameraY,cameraZ,world.shootx+random.uniform(-0.05,0.05), world.shooty+random.uniform(-0.05,0.05),world.shootz+random.uniform(-0.05,0.05)))
    
def begin(world):
    if world.startscreen == True:
        world.startscreen = False

def switch2(world):
    world.shotgun = True
    world.rifle= False
    world.ammo=6

def switch(world):
    world.rifle= True
    world.shotgun = False
    world.ammo=30




    
def updateWorld(world):
    if world.startscreen== True:
        onKeyPress(begin, "b")
        onKeyPress(switch, "g")
        onKeyPress(switch2, "f")        
        
    if world.startscreen== False:
        (oldx, oldy, oldz) = getCameraPosition()
        (cameraX, cameraY, cameraZ) = getCameraPosition()
        if isKeyPressed("s") and world.health>0:
            if world.shotgun == True:
                moveCameraBackward(0.75)
            if world.rifle == True:
                moveCameraBackward(0.75)
        if isKeyPressed("w")  and world.health>0:
            if world.shotgun == True:
                moveCameraForward(0.75)
            if world.rifle == True:
                moveCameraForward(0.75)
        if isKeyPressed("a") and world.health>0:
            if world.shotgun == True:
                strafeCameraLeft(0.75)
            if world.rifle == True:
                strafeCameraLeft(0.75)
        if isKeyPressed("d") and world.health>0:
            if world.shotgun == True:
                strafeCameraRight(0.75)
            if world.rifle == True:
                strafeCameraRight(0.75)
        if isKeyPressed("left arrow") and world.health>0:
            adjustCameraRotation(3,0,0)
            world.rotation+=3
        if isKeyPressed("right arrow") and world.health>0:
            adjustCameraRotation(-3,0,0)
            world.rotation-=3
        if world.win == True:
            if isKeyPressed("r"):
                startWorld(world)
        if world.firing==True:
            world.count+=1
            if world.count > 8:
                world.firing = False
                world.count=0
        
        
        '''if isKeyPressed("space"):
            adjustCameraPosition(0,1,0)
        if isKeyPressed("c"):
            adjustCameraPosition(0,-1,0)
        if isKeyPressed("up arrow"):
            adjustCameraRotation(0,1,0)
        if isKeyPressed("down arrow"):
            adjustCameraRotation(0,-1,0)'''
            
        
        onKeyPress(shoot,"space")
        
        
        if world.boss2alive==True:
            world.boomerangfire+=1
            world.boomerangfire2+=1
           
            world.missilecounter+=1
            
        for prize in world.myprizes:
            prize.update(world)
        for enemy in world.myenemies:
            enemy.update(world)
        for laser in world.mylasers:
            laser.update(world)
        for thing in world.thunder:
            thing.update(world)
       
        for enemy in world.myenemiesmall:
            enemy.update(world)

        for prize in world.myfinalprizes:
            prize.update(world)
        for bullet in world.mybullets:
            bullet.update(world)
        for boss in world.boss2:
            boss.update(world)
        for boss in world.boss3:
            boss.update(world)
        for missile in world.mymissiles:
            missile.update(world)
        for wall in world.mywalls2:
            wall.update(world)   
        for wall in world.mywalls3:
            wall.update(world)
        if world.spawn % 100 ==0:
            for enemy in world.myenemies:
                world.myenemiesmall.append(Smallenemy(world, enemy.x,enemy.y,enemy.z))
                world.myenemiesmall.append(Smallenemy(world,0,0,0))
        if world.boss1alive ==False:
            world.spawn=1
        if world.rifle == True:
            if world.ammo <30:
                world.ammoload+=1
                if world.ammoload % 7 ==0:
                    world.ammo+=1
        if world.shotgun== True:
            if world.ammo <6:
                world.ammoload +=1
                if world.ammoload % 30==0:
                    world.ammo+=1
        if world.pain == True:
            world.paincounter +=1
        if world.paincounter > 20:
            world.pain = False
            world.paincounter=0
        if world.bosshealth3 < 0:
            world.win = True
        
        
                    
                
        
        
        world.firerate+=1
        world.firerate3+=1
        world.firerate2+=1
        world.spawn+=1
        world.aggrocounter+=1
        world.aggrocounter2+=1
        
        if world.bosshealth < 0:
            world.boss1alive = False
            world.bosscounter = 0
            del world.myenemies[:]
            del world.myenemiesmall[:]
        
        if world.bosshealth2 < 0:
            world.boss2alive = False
            world.bosscounter2 = 0
            del world.boss2[:]
            del world.mymissiles[:]
    
        
        '''if world.time > 1000:
            updateTexture(world.ceiling, "sky_nightime.jpg")
        if world.time > 2000:
            world.time=0
        if world.time == 0:
            updateTexture(world.ceiling, "sky_daytime_blue.jpg")
            world.time+=1'''
        world.distance = (cameraX**2+cameraY**2+cameraZ**2)**0.5
       
        (cameraX, cameraY, cameraZ) = getCameraPosition()
        for wall in world.coords:
            if inWall(cameraX, cameraZ, wall.x ,wall.z):
                setCameraPosition(oldx, oldy, oldz)
        for wall in world.mywalls2:
            if inWall(cameraX, cameraZ, wall.x ,wall.z):
                setCameraPosition(oldx, oldy, oldz)
        for wall in world.mywalls3:
            if inWall(cameraX, cameraZ, wall.x ,wall.z):
                setCameraPosition(oldx, oldy, oldz)
        for door in world.mydoors:
            if inDoor(cameraX, cameraZ, door.x ,door.z) and world.bosscounter > 0:
                setCameraPosition(oldx, oldy, oldz)
        for door in world.mydoors:
            if inDoor(cameraX, cameraZ, door.x ,door.z) and world.bosscounter2 > 0:
                setCameraPosition(oldx, oldy, oldz)
        for door in world.mydoors:
            if inDoor(cameraX, cameraZ, door.x ,door.z) and world.bosscounter3 > 0:
                setCameraPosition(oldx, oldy, oldz)
        '''for bullet in world.mybullets:
            print bullet.x
            print bullet.y
            print bullet.z
            print'''

            
        
        
            



def drawWorld(world):
    if world.startscreen == False:
        draw3D(world.ceiling, 200,20,200,anglex=90)
        draw3D(world.floor, 200,0,200, anglex=90)
        for prize in world.myprizes:
            prize.draw(world)
        for enemy in world.myenemies:
            enemy.draw(world)
        
        for enemy in world.myenemiesmall:
            enemy.draw(world)
        for coord in world.coords:
            coord.draw()
        for door in world.mydoors:
            door.draw()
        for prize in world.myfinalprizes:
            prize.draw(world)
        for bullet in world.mybullets:
            bullet.draw(world) 
        for boss in world.boss2:
            boss.draw(world)
        for laser in world.mylasers:
            laser.draw(world)
        for missile in world.mymissiles:
            missile.draw(world)
        for boss in world.boss3:
            boss.draw(world)
        for wall in world.mywalls2:
            wall.draw(world)
        for wall in world.mywalls3:
            wall.draw(world)
        for thing in world.thunder:
            thing.draw(world)
        
        if world.health >0:

                
        
            clearCanvas2D(world.mycanvas)
            drawRectangle2D(world.mycanvas, 100, 30, world.health*5, 20, "black")
            fillRectangle2D(world.mycanvas, 100,30, world.health*5, 20, "green")
            if world.rifle == True:
                drawImage2D(world.mycanvas, world.gunfire2 , 440, 340, 0,2.8)
            if world.shotgun == True:
                drawImage2D(world.mycanvas, world.shotgunimage, 600,530,0,2.5)
            drawImage2D(world.mycanvas, world.crosshair , 400, 300, 0,0.4)
            drawImage2D(world.mycanvas, world.ammoimage, 100, 500,0,0.13)
            drawString2D(world.mycanvas, world.ammo, 170, 490 , 50, "white")
            drawString2D(world.mycanvas, "Health = "+str(world.health), 100, 30 , 30, "white")      
            if world.boss1alive == True:
                fillRectangle2D(world.mycanvas, 100,60, world.bosshealth*5, 20, "red")
                drawString2D(world.mycanvas, "BoneBoi, High Necromancer", 100, 60 , 30, "blue")
                
            if world.boss2alive == True:
                fillRectangle2D(world.mycanvas, 100,60, world.bosshealth2*5, 20, "red")
                drawString2D(world.mycanvas, "OWO and UWU Deranged Clown Brothers", 100, 60 , 30, "blue")
                #drawString2D(world.mycanvas, str(world.invincibilityframes), 200, 200 , 30, "white")
            if world.boss3alive == True:
                fillRectangle2D(world.mycanvas, 100,60, world.bosshealth3*5, 20, "red")
                drawString2D(world.mycanvas, "Eye See You, The Living Pun", 100, 60 , 30, "blue") 
            if world.firing == True:
                if world.rifle== True:
                    drawImage2D(world.mycanvas, world.gunfire , 440, 340, 0,2.8)
                if world.shotgun == True:
                    drawImage2D(world.mycanvas, world.shotgunimage2, 600, 530,0,2.5)
            if world.pain == True:
                drawImage2D(world.mycanvas, world.blood, 400, 400, 0, 1)
                   
           
        
        
        if world.health == 0:
            fillRectangle2D(world.mycanvas, 0, 0, 800, 600, "red")
            drawString2D(world.mycanvas,"YOU DIED",260,250, 80, "white")   
            
        #clearCanvas2D(world.mycanvas)
        if world.win == True:
            fillRectangle2D(world.mycanvas, 0, 0, 800, 600, "green")
            drawString2D(world.mycanvas,"YOU WIN",260,250, 80, "white")
            drawString2D(world.mycanvas, "press R to restart", 260, 400, 40,"white")
        

    draw2D(world.mycanvas, 0, 0)
    if world.startscreen == True:
        #drawString2D(world.mycanvas,"Press B to Begin",330,500, 30, "white")   
        drawImage2D(world.mycanvas,world.doom, 400,120,0, 0.7 )
        drawString2D(world.mycanvas,"Pow Pow, Kill things ",130,340, 30, "white")  
        drawString2D(world.mycanvas,"Shoot fast, shoot lots ",510,340, 30, "white")
        drawString2D(world.mycanvas,"Press F to select this weapon ",100,370, 30, "white")
        drawString2D(world.mycanvas,"Press G to select this weapon ",470,370, 30, "white")
        drawString2D(world.mycanvas,"WASD to move, left and right arrows to rotate camera",150,470, 30, "white")   
        drawString2D(world.mycanvas,"Space to shoot, Press B to Begin",270,530, 30, "white")   
        drawImage2D(world.mycanvas,world.shotgun3, 220,300,0, 0.3)
        drawImage2D(world.mycanvas,world.assault, 600,290,0, 0.3)
        
  

    
runGraphics(startWorld, updateWorld, drawWorld)
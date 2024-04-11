from app import app
from models import Hero, db
from random import choice
from test_data import heroes

class TestHero:
    """Test the heroes endpoints"""
    
    def init(self) -> None:
        Hero.query.delete()            
        db.session.commit()
        
    
    def test_create_hero(self):
        """Test posting a hero"""
        with app.app_context():
            self.init()
            
            hero = choice(heroes)
            response = app.test_client().post("/heroes", json=hero)
            
            assert response.status_code == 201
            assert response.content_type == "application/json"
            response = response.json
            for key in hero.keys():
                assert hero[key] == response[key]
            
    
    def test_get_heroes(self):
        """Test getting heroes"""
        with app.app_context():
            self.init()
            
            for hero in heroes:
                db.session.add(Hero(**hero))
            db.session.commit()
            
            hero = choice(heroes)
            response = app.test_client().get("/heroes")
            
            assert response.status_code == 200
            assert response.content_type == "application/json"
            heronames = [hero["name"] for hero in heroes]
            dbheroes = Hero.query.all()
            for hero in dbheroes:
                assert hero.name in heronames
            
         
    def test_get_hero_by_id(self):
        """Test get hero by id"""
        with app.app_context():
            self.init()
            
            response = app.test_client().get("/heroes/0")            
            assert response.status_code == 404
            
            hero = Hero(**choice(heroes))
            db.session.add(hero)
            db.session.commit()
            
            response = app.test_client().get("/heroes/"+str(hero.id))
            
            assert response.status_code == 200
            assert response.content_type == "application/json"
            response = response.json
            assert hero.name == response["name"]
            assert hero.super_name == response["super_name"]
            
    
    def test_update_hero(self):
        """Test updating hero and if there is 404 when not found"""
        with app.app_context():
            self.init()
            
            hero = Hero(**choice(heroes))
            db.session.add(hero)
            db.session.commit()
            
            newname = "Spider Man"
            
            response = app.test_client().patch("/heroes/0", json={"name":newname})
            assert response.status_code == 404
            
            response = app.test_client().patch("/heroes/"+str(hero.id), json={"name":newname})
            
            assert response.status_code == 200
            assert response.content_type == "application/json"
            response = response.json
            hero_dict = hero.to_dict()
            hero_dict["name"] = newname
            assert hero.name == response["name"]
            assert hero.super_name == response["super_name"]
            
            
    def test_get_hero_by_id_404(self):
        """Test delete hero and if we get status code 404 when not found"""
        with app.app_context():
            self.init()
            
            response = app.test_client().delete("/heroes/0")
            assert response.status_code == 404
            
            hero = Hero(**choice(heroes))
            db.session.add(hero)
            db.session.commit()
            
            response = app.test_client().delete("/heroes/"+str(hero.id))
            assert response.status_code == 204
            
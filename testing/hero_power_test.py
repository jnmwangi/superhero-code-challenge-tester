from app import app
from models import HeroPower, Hero, Power, db
from random import choice
from test_data import heroes, powers, strengths

class TestHeroPower:
    """Test the hero powers endpoints"""
    
    def init(self) -> None:
        
        Hero.query.delete()
        Power.query.delete()
        HeroPower.query.delete()
        
        for hero in heroes:
            db.session.add(Hero(**hero))
            
        for power in powers:
            db.session.add(Power(**power))
            
        db.session.commit()
        
        for hero in Hero.query.all():
            power = choice(Power.query.all())
            db.session.add(HeroPower(hero_id=hero.id, power_id=power.id, strength=choice(strengths)))
            
        db.session.commit()
        
    
    def hero_power(self):
        hero = choice(Hero.query.all())
        power = choice(Power.query.all())
        strength = choice(strengths)
        
        return {
            "hero_id": hero.id,
            "power_id": power.id,
            "strength": strength
        }
    
    def test_create_heropower(self):
        """Test posting a hero power"""
        with app.app_context():
            self.init()
            
            hero_power = self.hero_power()
            response = app.test_client().post("/hero_powers", json=hero_power)
            
            assert response.status_code == 201
            assert response.content_type == "application/json"
            response = response.json
            for key in hero_power.keys():
                assert hero_power[key] == response[key]
            
    
    def test_get_heropowers(self):
        """Test getting hero powers"""
        with app.app_context():
            self.init()
            
            response = app.test_client().get("/hero_powers")
            
            assert response.status_code == 200
            assert response.content_type == "application/json"
            
         
    def test_get_heropower_by_id(self):
        """Test get hero by id"""
        with app.app_context():
            self.init()
            
            response = app.test_client().get("/hero_powers/0")            
            assert response.status_code == 404
            
            hero_power = HeroPower(**self.hero_power())
            db.session.add(hero_power)
            db.session.commit()
            
            response = app.test_client().get("/hero_powers/"+str(hero_power.id))
            
            assert response.status_code == 200
            assert response.content_type == "application/json"
            response = response.json
            assert response["hero_id"] == hero_power.hero_id
            assert response['power_id'] == hero_power.power_id
            assert response["strength"] == hero_power.strength
            
    
    def test_update_heropower(self):
        """Test updating hero power and if there is 404 when not found"""
        with app.app_context():
            self.init()
            
            hero_power = HeroPower(**self.hero_power())
            db.session.add(hero_power)
            db.session.commit()
            
            new_streanth = choice(strengths)
            
            response = app.test_client().patch("/hero_powers/0", json={"strength":new_streanth})
            assert response.status_code == 404
            
            response = app.test_client().patch("/hero_powers/"+str(hero_power.id), json={"strength":new_streanth})
            
            assert response.status_code == 200
            assert response.content_type == "application/json"
            response = response.json
            assert response["hero_id"] == hero_power.hero_id
            assert response['power_id'] == hero_power.power_id
            assert response["strength"] == hero_power.strength
            
            
    def test_get_heropower_by_id_404(self):
        """Test delete hero power and if we get status code 404 when not found"""
        with app.app_context():
            self.init()
            
            response = app.test_client().delete("/hero_powers/0")
            assert response.status_code == 404
            
            hero_power = HeroPower(**self.hero_power())
            db.session.add(hero_power)
            db.session.commit()
            
            response = app.test_client().delete("/hero_powers/"+str(hero_power.id))
            assert response.status_code == 204
            

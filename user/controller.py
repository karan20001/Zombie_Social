from user.models import InventoryDetails, UserInventory, User
from user.libs.constants import constants

class UserController:

    def register_user_inventory(self, inventory, id):
        print(id)
        qset = InventoryDetails.objects.all()
        print(qset)
        for key, value in inventory.items():

            if key.lower() not in constants.InventoryConstant.INVENTORY_LIST:
                continue

            inventory_id = qset.filter(name = key).first().id
            print(key, inventory_id)
            inventory_obj = {
                "user_id" : id,
                "inventory_id" : inventory_id,
                "qty" : value
            }
            UserInventory.objects.create(**inventory_obj)


    def update_user_location(self, update_user_id, request_user_id, location):
        
        if(update_user_id != request_user_id):
            is_admin = User.objects.get(id = request_user_id).is_admin
            if(not is_admin):
                return constants.UserConstant.UserLocationConstants.PERMISSION_ERROR
        
        User.objects.filter(id=update_user_id).update(**location)
        return constants.UserConstant.UserLocationConstants.SUCCESSFULLY_UPDATED


    def mark_user(self, mark_user_id, reporter_user_id):

        user = User.objects.get(id = mark_user_id)

        if user.infected_3:
            return constants.UserConstant.UserMarkingConstants.ALREADY_SUCCESSFULLY_MARKED

        if(mark_user_id == reporter_user_id):
            user.infected_3 = reporter_user_id
            user.save(update_fields=['infected_3'])
            return constants.UserConstant.UserMarkingConstants.AWESOME_PERSON

        if user.infected_1:
            if user.infected_1 == reporter_user_id:
                return constants.UserConstant.UserMarkingConstants.ALREADY_MARKED

        else :
            user.infected_1 = reporter_user_id
            user.save(update_fields=['infected_1'])
            return constants.UserConstant.UserMarkingConstants.SUCCESSFULLY_MARKED

        if user.infected_2 :
            if user.infected_2 == reporter_user_id:
                return constants.UserConstant.UserMarkingConstants.ALREADY_MARKED
        
        else :
            user.infected_2 = reporter_user_id
            user.save(update_fields=['infected_2'])
            return constants.UserConstant.UserMarkingConstants.SUCCESSFULLY_MARKED

        if user.infected_3 :
            if user.infected_3 == reporter_user_id:
                return constants.UserConstant.UserMarkingConstants.ALREADY_MARKED
        
        else :
            user.infected_3 = reporter_user_id
            user.save(update_fields=['infected_3'])
            return constants.UserConstant.UserMarkingConstants.SUCCESSFULLY_MARKED    


    def trade_inventory(self, buyer_id, seller_id, requested_goods, offered_goods):

        user_qset = User.objects.filter(id__in = [buyer_id, seller_id]).only(id)

        for obj in user_qset:
            if obj.id == buyer_id:
                err = self.verify(obj.id, offered_goods)

                if err:
                    return constants.UserConstant.UserTradingConstants.OFFERED + err
                
            else:
                err = self.verify(obj.id, requested_goods)

                if err:
                    return constants.UserConstant.UserTradingConstants.REQUESTED + err
                
        if self.execute_trade(requested_goods, offered_goods):
            return constants.UserConstant.UserTradingConstants.SUCCESSFULLY_TRADED

        else:
            return constants.UserConstant.UserTradingConstants.UNFAIR_TRADE


    @staticmethod
    def verify(user_id, goods):

        user_inventory_qset = UserInventory.objects.filter(user_id = user_id)
        inventory_qset = InventoryDetails.objects.all()

        for key, value in goods.items():

            if key == constants.InventoryConstant.WATER:
                inventory_id = inventory_qset.get(name = key)
                return constants.UserConstant.UserTradingConstants.UNAVAILABLE_ERROR

            elif key == constants.InventoryConstant.FOOD and value != user_inventory_obj.food:
                return constants.UserConstant.UserTradingConstants.UNAVAILABLE_ERROR

            elif key == constants.InventoryConstant.MEDICATION and value != user_inventory_obj.medication:
                return constants.UserConstant.UserTradingConstants.UNAVAILABLE_ERROR

            elif key == constants.InventoryConstant.AMMUNITIONN and value != user_inventory_obj.ammunition:
                return constants.UserConstant.UserTradingConstants.UNAVAILABLE_ERROR
            
            else:
                return None


        @staticmethod
        def execute_trade(requested_goods, offered_goods):

            buy_value = 0
            sell_value = 0

            inventory_qset = InventoryDetails.objects.all()

            for obj in inventory_qset:
                if requested_goods.get(obj.name):
                    buy_value += obj.points

                if offered_goods.get(obj.name):
                    sell_value += obj.points

            if sell_value == buy_value:

                return True

            return False


    def generate_report(self):

        infected_percent, not_infected_percent = self.get_infected_not_infected_percentage()
        water, food, medication, ammunition = self.get_avg_resources()
        total_point_lost = self.get_total_point_lost()
        res = {
            "infected_user_percentage" : infected_percent,
            "not_infected_user_percentage" : not_infected_percent,
            "average_resources" : {
                "water" : water,
                "food" : food,
                "medication" : medication,
                "ammunition" : ammunition
            },
            "total_point_lost" : total_point_lost
        }
        return res


    @staticmethod
    def get_infected_not_infected_percentage():
        query = """
                    SELECT 
                        COUNT(CASE
                            WHEN infected_3 IS NULL THEN 1
                        END) AS not_infected,
                        COUNT(CASE
                            WHEN infected_3 != NULL THEN 1
                        END) AS infected,
                        id
                    FROM
                        user
                    WHERE
                        infected_3 IS NULL
                    GROUP BY id
                """

        qset = User.objects.raw(query)

        infected = 0
        not_infected = 0
        for obj in qset:
            infected += obj.infected
            not_infected += obj.not_infected

        total_users = infected + not_infected
        infected_percent = infected * 100 / total_users

        return infected_percent , 100 - infected_percent


    @staticmethod
    def get_avg_resources():

        query = """
                    SELECT 
                        inventory_details.id, inventory_details.name as name, avg(qty) as qty
                    FROM
                        inventory_details
                            INNER JOIN
                        user_inventory ON inventory_details.id=user_inventory.inventory_id
                    GROUP BY inventory_details.id;
                """

        qset = InventoryDetails.objects.raw(query)

        water = 0.0
        food = 0.0
        medication = 0.0
        ammunition = 0.0

        for obj in qset:

            if obj.name == constants.InventoryConstant.WATER :
                water = obj.qty

            elif obj.name == constants.InventoryConstant.FOOD:
                food = obj.qty

            elif obj.name == constants.InventoryConstant.MEDICATION:
                medication = obj.qty

            else :
                ammunition = obj.qty

        return water, food, medication, ammunition


    @staticmethod
    def get_total_point_lost():
        query = """
                    SELECT 
                        inventory_details.id, sum(points) as sum
                    FROM
                        inventory_details
                            JOIN
                        user_inventory ON inventory_details.id = user_inventory.inventory_id
                            JOIN
                        user ON user.id = user_inventory.user_id
                    where user.infected_3 is NULL
                    GROUP BY inventory_details.id;
                """

        qset = InventoryDetails.objects.raw(query)

        total_point_lost = 0
        for obj in qset:
            total_point_lost += obj.sum

        return total_point_lost
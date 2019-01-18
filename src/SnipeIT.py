import logging
import json
import requests
import html

SNIPE_IT_BASE_URL='http://188.68.32.95:8080'

JWT='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImRmYzY2YzRiZTM4MGMyOTk0MDYzMDA1MzhkODU5MDY5OGQzNThhOTg1OGEzMTVjM2YyNDllNWRlNGFhOTRkZDE5ZDhiYThiMWQ5MDJhMzQxIn0.eyJhdWQiOiIxIiwianRpIjoiZGZjNjZjNGJlMzgwYzI5OTQwNjMwMDUzOGQ4NTkwNjk4ZDM1OGE5ODU4YTMxNWMzZjI0OWU1ZGU0YWE5NGRkMTlkOGJhOGIxZDkwMmEzNDEiLCJpYXQiOjE1NDc4MDg1MzcsIm5iZiI6MTU0NzgwODUzNywiZXhwIjoxNTc5MzQ0NTM3LCJzdWIiOiIyIiwic2NvcGVzIjpbXX0.VfdxucJxcZKrmxaxESMab1Hrrmbzb2wM-66UE3XcH3cYSECGuTu7ynUNkPN8OYeF5qBYRKaK6kTJi50r3oT3xL5ApXrJLiJsPDaQIMyv_j8r1mZQatQxUVDP9uOer5CtiRPmZTZ2IR1MTXfp4T5FYWtYjB_nlspwTTrf8-u17gEzg1tj8RO6SQ8DjjN9NeFX9sCJ5bAZOv2Q_v_isBXcHUAzEvSs1EzGDevLjj8CgOvkWNfeQPRR12oxANJ5fJK6mUyrR92A1idLVxsZwpV8foP5DRUoRBZGL_CnvJ0rTqn4uT6GuRYlQB6a1CiBuD0ZlydMbzuoE5pYDbewLcGcozGrp68VLP7imQkE8TZ606bcpP4XDq0jPlYHF9IwS3ZFFi9k_yIEteE7vnYRQLsVV3_ZXUJAxJr3MYblx6DZi085CWlV3R9cxUDNX0kv7Sqj3foRY3DTWr5uhLzzkYghhXZ_BC3ir9rGtTmwbltYiaApr0K5_qvNbkcuMapa33ATL7KnzhMeKL0OKpwFwBm4YpfADdrUm3I8VFUUTVlkIZqRoTIwHQXInqRoC5ZmZv7R_4UOq7D_T3dLEX6SO8JdQmnf5J1ymGuMl_wCHxy_tIDbIM3PIGebFHjZqUnoWwEyjHsRzwIbVLQduHIzS_oOvmPOK1YRybbbas7xhAhrG20'

headers = {
        'Authorization': 'Bearer {}'.format(JWT),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        }

class SnipeIT():
    def checkout(self, asset_id, member_id, weight, image_path):
      user = self.get_user_by_employee_id(member_id)

      if user is None:
          return False

      user_id = user['id']

      note = {
              'weight': weight,
              'image_path': image_path
      }

      body = {
              'assigned_user': user_id, 
              'checkout_to_type': 'user',
              'note': json.dumps(note)
              }

      r = requests.post('{}/api/v1/hardware/{}/checkout'.format(SNIPE_IT_BASE_URL, asset_id), data = json.dumps(body), headers=headers)

      response = r.json()

      if r.status_code == 200 and response.get('status') != 'error':
          return True
      else:
          logging.error(r.json())
          return False


    def checkin(self, asset_id, weight, image_path):
      note = {
              'weight': weight,
              'image_path': image_path
      }

      body = {
              'note': json.dumps(note)
              }

      r = requests.post('{}/api/v1/hardware/{}/checkin'.format(SNIPE_IT_BASE_URL, asset_id), data = json.dumps(body), headers=headers)

      response = r.json()

      if r.status_code == 200 and response.get('status') != 'error':
          return True
      else:
          logging.error(r.json())
          return False

    def get_user_by_employee_id(self, member_id):
      params = {
              'search': member_id, 
      }

      r = requests.get('{}/api/v1/users'.format(SNIPE_IT_BASE_URL), params=params, headers=headers)

      response = r.json()

      if 'total' not in response or response['total'] == 0:
        logging.error('Unexpected response: {}'.format(response))
        return None

      results = response['rows']

      for user in results:
          if 'employee_num' in user and int(user['employee_num']) == member_id:
            return user

      logging.error('No user found with given member_id: {}'.format(response))
      return None

    def get_asset_by_id(self, asset_id):

      r = requests.get('{}/api/v1/hardware/{}'.format(SNIPE_IT_BASE_URL, asset_id), headers=headers)

      return r.json()

    def get_asset_last_activity(self, asset_id):
      params = {
              'item_id': asset_id,
              'item_type': 'asset',
              'sort': 'created_at',
              'order': 'desc',
              'offset': 0,
              'limit': 1
              }


      r = requests.get('{}/api/v1/reports/activity'.format(SNIPE_IT_BASE_URL), headers=headers, params=params)

      results = r.json()

      if 'total' not in results or int(results['total']) == 0:
        return None

      result = results['rows'][0]

      if result.get('note') is not None:
        try:
          result['note'] = json.loads(html.unescape(result['note']))
        except ValueError as e:
          pass

      return result




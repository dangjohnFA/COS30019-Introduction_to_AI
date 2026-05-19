import pandas as pd
import googlemaps # Cần cài đặt: pip install googlemaps

class RoadMap:
    def __init__(self, api_key, file_path='Full_Traffic_With_Validity_Cleaned.csv'):
        # Khởi tạo Google Maps Client
        self.gmaps = googlemaps.Client(key=api_key)
        
        # Load dữ liệu trạm từ file tối ưu nhất 
        self.df = pd.read_csv(file_path)
        self.geo_dict = self.df[['SCATS Number', 'NB_LATITUDE', 'NB_LONGITUDE']].drop_duplicates().set_index('SCATS Number').to_dict('index')

    def get_real_road_geometry(self, station_ids):
        """
        """
        if len(station_ids) < 2:
            return []

        full_curved_path = []
        
        for i in range(len(station_ids) - 1):
            origin = (self.geo_dict[station_ids[i]]['NB_LATITUDE'], 
                      self.geo_dict[station_ids[i]]['NB_LONGITUDE'])
            destination = (self.geo_dict[station_ids[i+1]]['NB_LATITUDE'], 
                           self.geo_dict[station_ids[i+1]]['NB_LONGITUDE'])
            
            # Gọi Directions API để lấy đường uốn lượn
            directions_result = self.gmaps.directions(
                origin,
                destination,
                mode="driving" # Đảm bảo đường đi bám theo lộ trình xe chạy
            )
            
            # Giải mã Polyline từ Google trả về thành danh sách tọa độ
            points = directions_result[0]['overview_polyline']['points']
            decoded_points = googlemaps.convert.decode_polyline(points)
            
            for pt in decoded_points:
                full_curved_path.append([pt['lat'], pt['lng']])
                
        return full_curved_path

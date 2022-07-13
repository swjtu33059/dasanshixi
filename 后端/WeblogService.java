package com.spark.service;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;


public class WeblogService {
    static String url ="jdbc:mysql://192.168.20.103:3306/test";
    static String username="root";
    static String password="123456";
    ArrayList<Double> rate = new ArrayList<>();

    public Map<String,Object> queryWeblogs() {
        Connection conn = null;
        PreparedStatement pst = null;
        String[] titleNames = new String[30];
        String[] titleCounts = new String[30];
        Map<String,Object> retMap = new HashMap<String, Object>();
        try{
            Class.forName("com.mysql.jdbc.Driver");
            conn = DriverManager.getConnection(url,username,password);
            String query_sql = "select titleName,count from webCount where 1=1 order by count desc limit 20";
            pst = conn.prepareStatement(query_sql);
            ResultSet rs = pst.executeQuery();
            int i = 0;
            while (rs.next()){
                String titleName = rs.getString("titleName");
                String titleCount = rs.getString("count");
                titleNames[i] = titleName;
                titleCounts[i] = titleCount;
                ++i;
            }
            retMap.put("titleName", titleNames);
            retMap.put("titleCount", titleCounts);
        }catch(Exception e){
            e.printStackTrace();
        }finally{
            try {
                if (pst != null) {
                    pst.close();
                }
                if (conn != null) {
                    conn.close();
                }

            }catch(Exception e){
                e.printStackTrace();
            }
        }
        return retMap;
    }

    public String[] titleCount() {
        Connection conn = null;
        PreparedStatement pst = null;
        String[] titleSums = new String[1];
        try{
            Class.forName("com.mysql.jdbc.Driver");
            conn = DriverManager.getConnection(url,username,password);
            String query_sql = "select count(1) titleSum from webCount";
            pst = conn.prepareStatement(query_sql);
            ResultSet rs = pst.executeQuery();
            if(rs.next()){
                String titleSum = rs.getString("titleSum");
                titleSums[0] = titleSum;
            }
        }catch(Exception e){
            e.printStackTrace();
        }finally{
            try{
                if (pst != null) {
                    pst.close();
                }
                if (conn != null) {
                    conn.close();
                }
            }catch(Exception e){
                e.printStackTrace();
            }
        }
        return titleSums;
    }

    public Map<String,Object> timeCount() {
        Connection conn = null;
        PreparedStatement pst = null;
        String[] timeIntervals = new String[30];
        String[] counts = new String[30];
        Map<String,Object> retMap = new HashMap<String, Object>();
        try{
            Class.forName("com.mysql.jdbc.Driver");
            conn = DriverManager.getConnection(url,username,password);
            String query_sql = "select timeInterval,count from timeCount where 1=1 order by timeInterval";
            pst = conn.prepareStatement(query_sql);
            ResultSet rs = pst.executeQuery();
            int i = 0;
            while (rs.next()){
                String timeInterval = rs.getString("timeInterval");
                String count = rs.getString("count");
                timeIntervals[i] = timeInterval;
                counts[i] = count;
                ++i;
            }
            retMap.put("timeInterval", timeIntervals);
            retMap.put("count", counts);
        }catch(Exception e){
            e.printStackTrace();
        }finally{
            try {
                if (pst != null) {
                    pst.close();
                }
                if (conn != null) {
                    conn.close();
                }

            }catch(Exception e){
                e.printStackTrace();
            }
        }
        return retMap;
    }

    public ArrayList rankCount() {
        Connection conn = null;
        PreparedStatement pst = null;
        //long commentCount = 0;
        long clickCount = 0;
        try{
            Class.forName("com.mysql.jdbc.Driver");
            conn = DriverManager.getConnection(url,username,password);
            /*
            String query_sql = "select sum(retorder) commentCount from rankRate";
            pst = conn.prepareStatement(query_sql);
            ResultSet rs1 = pst.executeQuery();
            if(rs1.next()){
                commentCount = rs1.getLong("commentCount");
            }
            */
            String count_sql = "select sum(cliorder) clickCount from ((select * from rankRate order by id desc limit 10) as tmp)";
            pst = conn.prepareStatement(count_sql);
            ResultSet rs2 = pst.executeQuery();
            if(rs2.next()){
                clickCount = rs2.getLong("clickCount");
            }
        }catch(Exception e){
            e.printStackTrace();
        }finally {
            try {
                if (pst != null) {
                    pst.close();
                }
                if (conn != null) {
                    conn.close();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        rate.add(clickCount / 1000.0);
        return rate;
    }
}
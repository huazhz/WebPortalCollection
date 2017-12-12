package com.example.lumi.portalwebcollection.util;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.example.lumi.portalwebcollection.R;
import com.example.lumi.portalwebcollection.model.New;

import org.w3c.dom.Text;

import java.io.InputStream;
import java.net.URL;
import java.util.List;

/**
 * Created by lumi on 2017/12/10.
 */

public class NewsAdapter extends ArrayAdapter<New>{
    private int resourceId;

    private ImageView newsImage;
    private TextView newsTitle;
    private Bitmap bitmap;
    private String ImgUrl;
    private int flag;
    public NewsAdapter(Context context, int resourceId, List<New> objects) {
        super(context, resourceId, objects);
        this.resourceId = resourceId;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        New news = getItem(position);
        View view;
        ViewHolder viewHolder;
//        if (convertView == null){
//            view = LayoutInflater.from(getContext()).inflate(resourceId, parent, false);
//            viewHolder = new ViewHolder();
//            viewHolder.newsImage = (ImageView) view.findViewById(R.id.news_image);
//            viewHolder.newsTitle = (TextView) view.findViewById(R.id.news_title);
//            view.setTag(viewHolder);
//        }else{
//            view = convertView;
//            viewHolder = (ViewHolder) view.getTag();
//        }
//        newsImage = viewHolder.newsImage;
//        newsTitle = viewHolder.newsTitle;

        view = LayoutInflater.from(getContext()).inflate(resourceId, parent, false);
        newsImage = (ImageView) view.findViewById(R.id.news_image);
        newsTitle = (TextView) view.findViewById(R.id.news_title);


        ImgUrl = news.getImgurl();
        if(ImgUrl.length() > 5){
            ViewGroup.LayoutParams params = newsImage.getLayoutParams();
            params.height = 160;
            params.width = 200;
            newsImage.setLayoutParams(params);
            setNetworkBitmap();
        }

        newsTitle.setText(news.getTitle());
        return view;
    }

    public void setNetworkBitmap() {

        bitmap = null;
        flag = 0;
        Runnable networkImg = new Runnable() {
            @Override
            public void run() {
                try {
                    URL conn = new URL(ImgUrl);
                    InputStream in = conn.openConnection().getInputStream();
                    bitmap = BitmapFactory.decodeStream(in);
                    in.close();
                } catch (Exception e) {
                    flag = 1;
                    e.printStackTrace();
                }
            }
        };
        new Thread(networkImg).start();

        while(bitmap == null && flag == 0){
            continue;
        }
        if(flag == 0){
            newsImage.setImageBitmap(bitmap);
        }
    }

    class ViewHolder{
        ImageView newsImage;
        TextView newsTitle;
    }
}

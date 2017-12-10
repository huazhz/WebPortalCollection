package com.example.lumi.portalwebcollection.util;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.example.lumi.portalwebcollection.R;
import com.example.lumi.portalwebcollection.model.New;

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
    public NewsAdapter(Context context, int resourceId, List<New> objects) {
        super(context, resourceId, objects);
        this.resourceId = resourceId;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        New news = getItem(position);
        View view = LayoutInflater.from(getContext()).inflate(resourceId, parent, false);
        newsImage = (ImageView) view.findViewById(R.id.news_image);
        newsTitle = (TextView) view.findViewById(R.id.news_title);
        ImgUrl = news.getImgurl();
        setNetworkBitmap();
        newsTitle.setText(news.getTitle());
        return view;
    }

    public void setNetworkBitmap() {

        bitmap = null;

        Runnable networkImg = new Runnable() {
            @Override
            public void run() {
                try {
                    URL conn = new URL(ImgUrl);
                    InputStream in = conn.openConnection().getInputStream();
                    bitmap = BitmapFactory.decodeStream(in);
                    in.close();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        };
        new Thread(networkImg).start();

        while(bitmap == null){
            continue;
        }
        newsImage.setImageBitmap(bitmap);
    }
}

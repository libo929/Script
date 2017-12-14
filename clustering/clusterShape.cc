// This script is to test algorithm of distiguishing 
// cluster shape, i.e., blob or track-like

class Point
{
public:
	Point()
	{
		X1.SetXYZ(10000., 10000., 10000.);
		X2.SetXYZ(10000., 10000., 10000.);
	}

	TVector3 X0;
	TVector3 X1;
	TVector3 X2;
};

void GenBlob(std::vector<Point>& points)
{
	int numHits = gRandom->Uniform(5, 20);

	//std::cout << "hit number: " << numHits << std::endl;

	for(int iHit = 0; iHit < numHits; ++iHit)
	{
		double x = gRandom->Uniform(10, 20);
		double y = gRandom->Uniform(30, 100);
		double z = gRandom->Uniform(10, 300);

		Point point;
	   	point.X0 = TVector3(x, y, z);

		points.push_back(point);
	}
}

void GenLine(std::vector<Point>& points)
{
	int numHits = int(gRandom->Uniform(5, 20));

	//std::cout << "hit number: " << numHits << std::endl;
	const double SIGMA = 1;

	for(int iHit = 0; iHit < numHits; ++iHit)
	{
		double x, y, z;

		x =  (2. * iHit + 100.) + gRandom->Uniform(0, 0.5);

		if(iHit < 10) 
		{
			y =  3. * x  + gRandom->Uniform(-SIGMA, SIGMA);
			z = -2. * x  + gRandom->Uniform(-SIGMA, SIGMA);
		}
		else
		{
			y =  5. * x  + gRandom->Uniform(-SIGMA, SIGMA);
			z = -3. * x  + gRandom->Uniform(-SIGMA, SIGMA);
		}

		Point point;
	   	point.X0 = TVector3(x, y, z);

		points.push_back(point);
	}
}

double getClusterShapeCoeff(int rnd)
{
	gRandom->SetSeed(rnd);
	////// hits generation
	std::vector<Point> points;
	//GenBlob(points);
	GenLine(points);

	int numHits = points.size();

	////// get the nearest hit distance
	for(int iHit = 0; iHit < numHits; ++iHit)
	{
	    for(int jHit = 0; jHit < numHits; ++jHit)
		{
			if(iHit==jHit) continue;

			Point& PointI = points.at(iHit);
			Point& PointJ = points.at(jHit);

			TVector3 dist = PointJ.X0 - PointI.X0;
			//dist.Print();

			if(dist.Mag() < PointI.X1.Mag()) PointI.X1 = dist;
			if(dist.Mag() > PointI.X1.Mag() && dist.Mag() < PointI.X2.Mag()) PointI.X2 = dist;
		}
	}

	////// print hit
	double meanHitDist = 0.;

	for(int iHit = 0; iHit < numHits; ++iHit)
	{
		Point& PointI = points.at(iHit);

		TVector3& point0 = PointI.X0;
		TVector3& point1 = PointI.X1;
		TVector3& point2 = PointI.X2;

		meanHitDist += point1.Mag();

		//point0.Print();
		//point1.Print();
		//point2.Print();
		//cout << "----------" << endl;
	}

	meanHitDist /= numHits;

	//cout << "mean distance: " << meanHitDist << endl;

	TH1F h("hist", "hist", 100, -1000, 1000);

	for(int iHit = 0; iHit < numHits; ++iHit)
	{
		Point& PointI = points.at(iHit);

		double d1 = PointI.X1.Mag();
		double d2 = PointI.X2.Mag();

		double angle1 = PointI.X1.Angle(PointI.X2);
		double angle2 = TMath::Pi() - PointI.X1.Angle(PointI.X2);
		double angle = min(angle1, angle2);
		//cout << "--> angle: " << angle << endl;
		
		double coeff = angle * TMath::Exp(-(d1-d2)*(d1-d2)/(meanHitDist*meanHitDist));

		h.Fill(coeff);
		//cout << "-----coeff: " << coeff << endl;
	}

	return h.GetRMS();

	//cout << "hist RMS: " << h.GetRMS() << endl;
}

void clusterShape()
{
	TH1F* hist = new TH1F("", "", 100, -1, 1);

	for(int iRnd = 0; iRnd < 100; ++iRnd)
	{
		double clusterCoeff = getClusterShapeCoeff(iRnd);
		//cout << "cluster: " << clusterCoeff << endl;
		hist->Fill(clusterCoeff);
	}

	hist->Draw();
}
